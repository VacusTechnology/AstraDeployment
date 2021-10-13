import mysql.connector
import datetime

# import statement for creating logs
import yaml
import logging.config

import configparser


def weekly(db):
    try:
        cursor = db.cursor()
        currentDate = datetime.date.today()
        sqldayavg = "select asset_id,round(avg(p.co2)) as co2, round(avg(p.tvoc)) as tvoc, p.time from" \
                    " (select asset_id,co2,tvoc,date_format(timestamp-interval minute(timestamp)%30 minute, '%Y-%m-%d %H:%i') as time " \
                    "from sensor_dailyiaq where timestamp like '" + str(currentDate) + "%'" \
                    "group by date_format(timestamp-interval minute(timestamp)%30 minute, '%Y-%m-%d %H:%i'), co2, tvoc,asset_id) as p  group by p.time, asset_id;"
        cursor.execute(sqldayavg)
        result = cursor.fetchall()
        if result is not None:
            for row in result:
                sql = "insert into sensor_weeklyiaq (co2, tvoc, timestamp, asset_id) values(" + str(
                    row[1]) + "," + str(row[2]) + ",'" + str(row[3]) + "'," + str(row[0]) + ");"
                cursor.execute(sql)
                db.commit()
            logger.info("Weekly iaq data stored.")
            return True

    except Exception as err:
        logger.info("Error: ", str(err))
        return False

    finally:
        cursor.close()


def monthly(db):
    try:
        cursor = db.cursor()
        today = datetime.datetime.today().date()
        sql = "select distinct DATE(timestamp) as time,asset_id,round(avg(co2)),round( avg(tvoc)) from sensor_weeklyiaq where timestamp like '" + \
            str(today)+"%' group by asset_id, time;"

        cursor.execute(sql)
        result1 = cursor.fetchall()
        if result1 is not None:
            for row in result1:
                sql = "insert into  sensor_monthlyiaq (co2, tvoc, timestamp, asset_id) values(" + str(
                    row[2]) + "," + str(row[3]) + ",'" + str(row[0]) + "'," + str(row[1]) + ");"
                cursor.execute(sql)
                db.commit()
            logger.info("Monthly iaq data stored.")

    except Exception as err:
        logger.info("Error: ", str(err))

    finally:
        cursor.close()


if __name__ == '__main__':

    with open('/root/AstraDeployment/logs/logging_error.yaml', 'r') as stream:
        logger_config = yaml.load(stream, yaml.FullLoader)
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger('IAQ -')

    config = configparser.RawConfigParser()
    config.read('db_details.properties')

    host = config.get('DatabaseSection', 'database.host')
    dbname = config.get('DatabaseSection', 'database.dbname')
    user = config.get('DatabaseSection', 'database.user')
    password = config.get('DatabaseSection', 'database.password')

    # Creating database connection object and connecting to data base
    db = mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=dbname
    )

    if weekly(db):
        monthly(db)

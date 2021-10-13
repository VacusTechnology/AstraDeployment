from calendar import monthrange
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
        sqldayavg = "select count(distinct(tagid_id)) as count, substring(timestamp, 1, 16) timestamp, zoneid_id from zones_zonetracking where timestamp like '" + \
            str(currentDate)+"%' group by date_format(timestamp-interval minute(timestamp) % 30 minute, '%Y-%m-%d %H:%i'), zoneid_id"
        cursor.execute(sqldayavg)
        result = cursor.fetchall()
        if result is not None:
            for row in result:
                sql = "insert into zones_weeklyzonetracking(count,timestamp,zoneid_id) values("+str(
                    row[0])+",'"+str(row[1])+"',"+str(row[2])+");"
                cursor.execute(sql)
                db.commit()
            logger.info("Weekly data inserted successfully.")

    except Exception as err:
        logger.info("Error:", str(err))

    finally:
        cursor.close()


def monthly(db):
    try:
        cursor = db.cursor()
        currentDate = datetime.date.today()
        sqldayavg = "select count(distinct(tagid_id)) as count, substring(timestamp, 1, 11)  timestamp, zoneid_id from zones_zonetracking where timestamp like '" + \
            str(currentDate)+"%' group by zoneid_id"
        cursor.execute(sqldayavg)
        result = cursor.fetchall()
        if result is not None:
            for row in result:
                sql = "insert into zones_monthlyzonetracking(count,timestamp,zoneid_id) values("+str(
                    row[0])+",'"+str(row[1])+"',"+str(row[2])+");"
                cursor.execute(sql)
                db.commit()
            logger.info("Monthly data inserted successfully.")

    except Exception as err:
        logger.info("Error:", str(err))

    finally:
        cursor.close()


if __name__ == '__main__':

    with open('/root/AstraDeployment/logs/logging_error.yaml', 'r') as stream:
        logger_config = yaml.load(stream, yaml.FullLoader)
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger('ZoneTracking -')

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

    weekly(db)
    monthly(db)

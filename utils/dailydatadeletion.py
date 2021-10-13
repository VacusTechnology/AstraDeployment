import mysql.connector
import datetime

# import statement for creating logs
import yaml
import logging.config

import configparser


def logAndClearData():
    try:

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

        # creating different datetime objects
        currentDate = datetime.datetime.today()
        previousday = currentDate - datetime.timedelta(days=1)
        daybeforeyesterday = currentDate - datetime.timedelta(days=2)
        week = currentDate - datetime.timedelta(days=7)

        # creating cursor object to execute sql queries
        cursor = db.cursor()
        logger.info("Creating cursor object.")

        # deleting today's alert data
        alert = """delete from alert_alert where timestamp like %s"""
        par = str(previousday)+"%"
        val = (par,)
        cursor.execute(alert, val)
        logger.info("Alert data deleted.", str(previousday))

        # deleting previous day social distancing data
        calculation = """delete from  employee_distancecalculation  where timestamp like %s """
        par = str(daybeforeyesterday)+"%"
        val = (par,)
        cursor.execute(calculation, val)
        logger.info("Social distanceing data deleted.",
                    str(daybeforeyesterday))

        # deleting today's thermal map data
        dailydata = """delete from sensor_dailytemperaturehumidity where timestamp like %s"""
        par = str(previousday)+"%"
        val = (par,)
        cursor.execute(dailydata, val)
        logger.info("Thermal data deleted.", str(previousday))

        # deleting last week data from weekly sensor table
        weeklydata = """delete from  sensor_weeklytemperaturehumidity  where timestamp like %s """
        par = str(week)+"%"
        val = (par,)
        cursor.execute(weeklydata, val)
        logger.info("Weekly Thermal data deleted.", str(week))
        # commitng the changes to the database
        db.commit()

        # deleting today's thermal map data
        dailydata = """delete from sensor_dailyiaq where timestamp like %s"""
        par = str(previousday)+"%"
        val = (par,)
        cursor.execute(dailydata, val)
        logger.info("Thermal data deleted.", str(previousday))

        # deleting last week data from weekly sensor table
        weeklydata = """delete from  sensor_weeklyiaq  where timestamp like %s """
        par = str(week)+"%"
        val = (par,)
        cursor.execute(weeklydata, val)
        logger.info("Weekly Thermal data deleted.", str(week))
        # commitng the changes to the database
        db.commit()

    except Exception as err:
        logger.info("Error : ", str(err))

    finally:
        # Closing cursor object
        cursor.close()
        logger.info("Closed cursor object.")


# the program execution starts from here
if __name__ == "__main__":
    with open('/root/AstraDeployment/logs/logging_error.yaml', 'r') as stream:
        logger_config = yaml.load(stream, yaml.FullLoader)
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger('DailyDeletion -')

    logAndClearData()

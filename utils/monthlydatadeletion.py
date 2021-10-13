import mysql.connector
import datetime
import dateutil.relativedelta

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
        todays_date = datetime.datetime.today()
        month = todays_date - dateutil.relativedelta.relativedelta(months=1)
        previousmonth = (str(month)[0:7])

        # creating cursor object to execute sql queries
        cursor = db.cursor()
        logger.info("Creating cursor object.")

        # deleting last month data from theraml map table
        monthlydata = """delete from sensor_monthlytemperaturehumidity where timestamp like %s"""
        par = str(previousmonth)+"%"
        val = (par,)
        cursor.execute(monthlydata, val)
        logger.info("Thermal data deleted.", str(previousmonth))

        # deleting last month data from iaq table
        monthlydata = """delete from sensor_monthlyiaq where timestamp like %s"""
        par = str(previousmonth)+"%"
        val = (par,)
        cursor.execute(monthlydata, val)
        logger.info("IAQ data deleted.", str(previousmonth))

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
    logger = logging.getLogger('MonthlyDeletion -')

    logAndClearData()

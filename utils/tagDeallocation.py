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

        currentDate = datetime.datetime.today()

        # creating cursor object for executing the sql queries
        cursor = db.cursor()
        tagdeallocation = """update employee_employeeregistration set tagid_id = %s"""
        val = (None, )
        cursor.execute(tagdeallocation, val)

        # commitng the changes to the database
        db.commit()

    except Exception as err:
        logger.info("Error: ", str(err))

    finally:
        cursor.close()


# the program execution starts from here
if __name__ == "__main__":

    with open('/root/AstraDeployment/logs/logging_error.yaml', 'r') as stream:
        logger_config = yaml.load(stream, yaml.FullLoader)
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger('TagDeallocation -')

    logAndClearData()

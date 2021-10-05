import paho.mqtt.client as paho
import json
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import yaml
import logging
import logging.config

from tables import *
logger = logging.getLogger(__name__)

engine = create_engine(
    "mysql+pymysql://vacus:vacus@127.0.0.1/vacusdb", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
BROKER_ENDPOINT = "astra.vacustech.in"
PORT = 1883
topic = "tracking"


def on_message(client, userdata, message):
    logger.info("Data received")
    serializedJson = message.payload.decode('utf-8')
    jsonData = json.loads(serializedJson)
    storeData(jsonData)


def storeData(jsonData):
    try:
        print(jsonData)
        timeStamp = datetime.datetime.now()

        masterid = jsonData["master"]
        """Retrieveing Master Gateway object"""
        master = session.query(gateway_mastergateway).filter(
            gateway_mastergateway.gatewayid == masterid).first()

        if master is not None:
            """ Updating master gateway lastseen """
            floor_id = master.floor_id
            master.lastseen = timeStamp
            session.commit()

            """ Iterating through all array of asset """
            for elem in jsonData["assets"]:
                """ Retrieveing Slave Gateway object """
                slave = session.query(gateway_slavegateway).filter(
                    gateway_slavegateway.gatewayid == elem["slaveaddress"]).first()
                if slave is not None:
                    """ Updating slave gateway lastseen """
                    slave.lastseen = timeStamp
                    session.commit()

                """ Retrieveing Employee Object"""
                employee = session.query(employee_tag).filter(
                    employee_tag.tagid == elem["macaddress"]).first()
                if employee:
                    """ Updating health, tracking and alert data for employee tag """
                    employee.lastseen = timeStamp
                    employee.battery = elem["battery"]
                    employee.floor_id = floor_id
                    employee.x = elem['X']
                    employee.y = elem['Y']
                    session.commit()

                    if elem["alert"] > 0:
                        employee_alert = alert_alert(id=alert_alert.id, value=elem["alert"], timestamp=timeStamp,
                                                     asset_id=employee.id)
                        session.add(employee_alert)
                        session.commit()

                    zone = session.query(zones_zones).filter(
                        zones_zones.x1 < elem['X'], zones_zones.x2 >= elem['X'], zones_zones.y1 < elem['Y'], zones_zones.y2 >= elem['Y']).first()
                    if zone:
                        track = ZoneTracking(
                            id=ZoneTracking.id, zoneid_id=zone.id, tagid_id=employee.id, timestamp=timestamp)
                        session.add(track)
                        session.commit()
                else:
                    pass

                """ Retrieveing Temperature/Humidity object"""
                temp = session.query(sensor_temperaturehumidity).filter(
                    sensor_temperaturehumidity.macid == elem["macaddress"]).first()
                if temp:
                    """ Updating temp, humid, health data of particular asset """
                    temp.temperature = elem["temp"]
                    temp.humidity = elem["humidity"]
                    temp.lastseen = timeStamp
                    temp.floor_id = floor_id
                    temp.battery = elem["battery"]
                    session.commit()

                    dailydata = sensor_dailytemperaturehumidity(
                        temperature=elem["temp"],
                        humidity=elem["humidity"], asset_id=temp.id,
                        timestamp=timeStamp)
                    session.add(dailydata)
                    session.commit()
                else:
                    pass

                """ Retrieveing IRQ sensor object """
                iaq = session.query(sensor_iaq).filter(
                    sensor_iaq.macid == elem["macaddress"]).first()
                if iaq:
                    """ Updating lastseen and battery status"""
                    iaq.lastseen = timeStamp
                    iaq.battery = elem["battery"]
                    # iaq.co2 = elem[""]
                    # iaq.tvoc = elem[""]
                    session.commit()

                    # dailydata = sensor_dailyiaq(
                    #     co2=elem[""], tvoc=elem[""], asset_id=iaq.id, timestamp=timeStamp)
                    # session.add(dailydata)
                    # session.commit()

                else:
                    pass

                """ Retrieveing Signal repeater object """
                signal = session.query(signalrepeator).filter(
                    signalrepeator.macid == elem["macaddress"]).first()
                if signal:
                    """ Updating lastseen """
                    signal.lastseen = timeStamp
                    session.commit()
                else:
                    pass

    except Exception as err:
        print(err)
       # logger.info("Error: ", str(err))


def on_connect(client, userdata, flags, rc):
    logger.info("Connected to broker")
    client.subscribe(topic)  # subscribe topic test


def on_disconnect(client, userdata, rc):
    if rc != 0:
        logger.info("Disconnection from broker, Reconnecting...")
        systemcon()
        client.subscribe(topic)  # subscribe topic test


def systemcon():
    st = 0
    try:
        st = client.connect(BROKER_ENDPOINT, PORT)  # establishing connection
    except:
        st = 1
    finally:
        if (st != 0):
            logger.info("Connection failed, Reconnecting...")
            time.sleep(5)
            systemcon()


if __name__ == "__main__":

    # with open('/home/ec2-user/logs/logging_tracking.yaml', 'r') as stream:
    #     logger_config = yaml.load(stream, yaml.FullLoader)
    # logging.config.dictConfig(logger_config)
    # logger = logging.getLogger('Tracking -')

    client = paho.Client()  # create client object
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    systemcon()
    client.subscribe(topic)  # subscribe topic test
    client.loop_forever()

    while True:
        pass

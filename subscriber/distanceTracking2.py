"""  """

import paho.mqtt.client as paho
import json
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import yaml
import logging.config

from tables import *

engine = create_engine(
    "mysql+pymysql://astra:astra@127.0.0.1/vacusdb", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()
BROKER_ENDPOINT = "astramaster2.vacustech.in"
PORT = 1883
topic = "distance_tracking"


def on_message(client, userdata, message):
    logger.info("Data received")
    serializedJson = message.payload.decode('utf-8')
    jsonData = json.loads(serializedJson)
    storeData(jsonData)


def storeData(jsonData):
    try:
        slave = session.query(gateway_slavegateway).filter(
            gateway_slavegateway.gatewayid == jsonData["slaveaddress"]).first()
        if slave:
            timestamp = datetime.datetime.now()
            for list in jsonData["assets"]:
                tag1 = session.query(employee_tag).filter(
                    employee_tag.tagid == list["tag1"]).first()
                if tag1:
                    name1 = session.query(employee_registration).filter(
                        employee_registration.tagid_id == tag1.id).first()
                    if name1:
                        for matched in list["matched"]:
                            tag2 = session.query(employee_tag).filter(
                                employee_tag.tagid == matched["Tag2"]).first()
                            if tag2:
                                name2 = session.query(employee_registration).filter(
                                    employee_registration.tagid_id == tag2.id).first()
                                if name2:
                                    dist = employee_distancetracking(
                                        id=employee_distancetracking.id, tag1_id=name1.id, tag2_id=name2.id, distance=matched["distance"], timestamp=timestamp)
                                    session.add(dist)
                                    session.commit()
                                    print("inseeted")

    except Exception as error:
        logger.info("Error: ", str(err))


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

    with open('/home/ubuntu/logs/logging_distancetracking.yaml', 'r') as stream:
        logger_config = yaml.load(stream, yaml.FullLoader)
    logging.config.dictConfig(logger_config)
    logger = logging.getLogger('TenthFloor -')

    client = paho.Client()  # create client object
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect

    systemcon()
    client.subscribe(topic)  # subscribe topic test
    client.loop_forever()

import paho.mqtt.client as mqtt
import time
import json
import datetime
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidName
import __future__

def on_connect(mqtt, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    mqtt.subscribe("/opcua/#")

def on_message(mqtt, userdata, msg, collection):
    receiveTime = datetime.datetime.now()
    message = msg.payload.decode("utf-8")
    isfloatValue = False
    try:
        # Convert the string to a float so that it is stored as a number and not a string in the database
        val = float(message)
        isfloatValue = True
    except:
        isfloatValue = False

    if isfloatValue:
        print(str(receiveTime) + ": " + msg.topic + " " + str(val))
        post = {"time": receiveTime, "topic": msg.topic, "value": val}
    else:
        print(str(receiveTime) + ": " + msg.topic + " " + message)
        post = {"time": receiveTime, "topic": msg.topic, "value": message}

    collection.insert_one(post)

def mongodb_connection():
    mongodb_conn = os.environ['mongodb_connnection']
    mongoClient = MongoClient(mongodb_conn)
    db = mongoClient.plc_poc_db
    collection = db.plc_poc
    return collection

def mongodb_connection():
    mqtt_server_conn = os.environ['mqtt_conn']
    mqttc = mqtt.Client(mqtt_server_conn)
    mqttc.on_connect = on_connect
    mqttc.on_message = on_message
    mqttc.loop_forever()

def start_listening():
    mongodb_connection()

def function_handler(event, context):
    return



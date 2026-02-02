from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import threading
import json
from datetime import datetime, timezone

from settings import load_settings
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write_api import WritePrecision

import paho.mqtt.client as mqtt

import paho.mqtt.subscribe as subscribe

influx_config = {
    "url": "http://localhost:8087",
    "token": "my-super-secret-token",
    "org": "moja_org",
    "bucket": "tvoj_bucket"
}

def on_connect(client, userdata, flags, rc):
    client.subscribe("device/+")

def on_message(client, userdata, msg):
    print(msg.topic+" "+msg.payload.decode("utf-8"))
    topic = msg.topic
    payload = json.loads(msg.payload.decode("utf-8"))
    match topic:
        case "device/dpir":
            for single_data in payload:
                add_point("DPIR", single_data)
        
        case "device/dus":
            for single_data in payload:
                add_point("DUS", single_data)
        case "device/ds":
            for single_data in payload:
                add_point("DS", single_data)
                
        case "device/dl":
            add_point("DL", payload)
        
        case "device/dms":
                measurment_time = datetime.fromtimestamp(payload['timestamp'], tz=timezone.utc)
                point = Point("DMS") \
                .tag("name", payload["name"]) \
                .field("simulated", payload["simulated"]) \
                .field("value", payload["value"])\
                .field("attempt", payload["attempt"])\
                .time(measurment_time)
            
                write_api.write(bucket="moj_bucket", record=point, org="moja_org")

        case "device/db":
            for single_data in payload:
                add_point("DB", single_data)

def add_point(measurment_name, data):
    measurment_time = datetime.fromtimestamp(data['timestamp'], tz=timezone.utc)
    point = Point(measurment_name) \
    .tag("name", data["name"]) \
    .field("simulated", data["simulated"]) \
    .field("value", data["value"])\
    .time(measurment_time, WritePrecision.NS)
    
    write_api.write(bucket="moj_bucket", record=point, org="moja_org")

app = Flask(__name__)

if __name__ == "__main__":
    print("FLASK POKRENUT...")
    settings = load_settings()
    influx_client = InfluxDBClient(url=influx_config['url'], token=influx_config['token'])
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    
    data = {
        "influx_client": influx_client,
        "write_api": write_api,
        "settings": settings
    }
    
    client = mqtt.Client(userdata = data )
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("localhost", 1883, 60)

    client.loop_forever()
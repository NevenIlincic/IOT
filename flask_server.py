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
    "url": "http://192.168.107.153:8087", ##PROMENI NA IP UCIONICE
    "token": "my-super-secret-token",
    "org": "moja_org",
    "bucket": "tvoj_bucket"
}

def on_connect(client, userdata, flags, rc):
    client.subscribe("devices")

def on_message(client, userdata, msg):
    #print(msg.topic+" "+msg.payload.decode("utf-8"))
    topic = msg.topic
    payload = json.loads(msg.payload.decode("utf-8"))
    
    if type(payload) == list:
        for single_data in payload:
            name = single_data["name"]
            
            match name:
                case "dpir":
                    add_point("DPIR", single_data)
                
                case "dus":
                    add_point("DUS", single_data)
                case "ds":
                    add_point("DS", single_data)
                        
                case "dl":
                    add_point("DL", single_data)
                
                case "db":
                    print(single_data)
                    add_point("DB", single_data)
                
                case "lcd":
                    print(single_data)
                    add_point("LCD", single_data)
                case "dht":
                    measurment_time = datetime.fromtimestamp(single_data['timestamp'], tz=timezone.utc)
                    point = Point("DHT") \
                    .tag("name", single_data["name"]) \
                    .field("simulated", single_data["simulated"]) \
                    .field("temperature", single_data["temperature"])\
                    .field("humidity", single_data["humidity"])\
                    .time(measurment_time)
            
                    write_api.write(bucket="moj_bucket", record=point, org="moja_org")
                case "gyroscope":
                    measurment_time = datetime.fromtimestamp(single_data['timestamp'], tz=timezone.utc)
                    point = Point("GYROSCOPE") \
                    .tag("name", single_data["name"]) \
                    .field("simulated", single_data["simulated"]) \
                    .field("rotation", single_data["rotation"])\
                    .field("acceleration", single_data["acceleration"])\
                    .time(measurment_time)
            
                    write_api.write(bucket="moj_bucket", record=point, org="moja_org")
                    
    elif type(payload) == dict:
        name = payload["name"]
        match name:
            case "dms":
                measurment_time = datetime.fromtimestamp(payload['timestamp'], tz=timezone.utc)
                point = Point("DMS") \
                .tag("name", payload["name"]) \
                .field("simulated", payload["simulated"]) \
                .field("value", payload["value"])\
                .field("attempt", payload["attempt"])\
                .time(measurment_time)
            
                write_api.write(bucket="moj_bucket", record=point, org="moja_org")
                
            case "alarm":
                measurment_time = datetime.fromtimestamp(payload['timestamp'], tz=timezone.utc)
                point = Point("ALARM") \
                .tag("name", payload["name"]) \
                .field("value", payload["value"])\
                .time(measurment_time)
            
                write_api.write(bucket="moj_bucket", record=point, org="moja_org")
                
            case "ir":
                print(payload)
                measurment_time = datetime.fromtimestamp(payload['timestamp'], tz=timezone.utc)
                point = Point("IR") \
                .tag("name", payload["name"]) \
                .field("value", payload["value"]) \
                .field("simulated", payload["simulated"]) \
                .time(measurment_time)
            
                write_api.write(bucket="moj_bucket", record=point, org="moja_org")
            
            case "rgb":
                measurment_time = datetime.fromtimestamp(payload['timestamp'], tz=timezone.utc)
                point = Point("RGB") \
                .tag("name", payload["name"]) \
                .field("value", payload["value"]) \
                .field("simulated", payload["simulated"]) \
                .time(measurment_time)
            
                write_api.write(bucket="moj_bucket", record=point, org="moja_org")
                
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
    client.connect("192.168.107.153", 1883, 60) #PROMENI NA IP UCIONICE

    client.loop_forever()
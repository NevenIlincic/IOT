from flask import Flask, jsonify, request
from flask_cors import CORS
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
    "url": "http://localhost:8087", ##PROMENI NA IP UCIONICE
    "token": "my-super-secret-token",
    "org": "moja_org",
    "bucket": "tvoj_bucket"
}

client = None
system_status_storage = {
    "alarm_state": "NOT_ACTIVE",
    "num_people": 0,
    "security_system_state": "SYSTEM NOT ACTIVE"
}

def on_connect(client, userdata, flags, rc):
    client.subscribe("devices")
    client.subscribe("people_in_system")

def on_message(client, userdata, msg):
    #print(msg.topic+" "+msg.payload.decode("utf-8"))
    topic = msg.topic
    payload = json.loads(msg.payload.decode("utf-8"))
    
    
    if type(payload) == list:
        for single_data in payload:
            name = single_data["name"]
            
            match name:
                case "dpir_1":
                    print(single_data)
                    add_point("DPIR_1", single_data)
                case "dpir_2":
                    add_point("DPIR_2", single_data)
                case "dpir_3":
                    add_point("DPIR_3", single_data)
                
                case "dus_1":
                    add_point("DUS_1", single_data)
                case "dus_2":
                    add_point("DUS_2", single_data)
                    
                case "ds_1":
                    print(single_data)
                    add_point("DS_1", single_data)
                case "ds_2":
                    print(single_data)
                    add_point("DS_2", single_data)
                case "btn":
                    add_point("BTN", single_data)
                        
                case "dl":
                    add_point("DL", single_data)
                
                case "db":
                    print(single_data)
                    add_point("DB", single_data)
                
                case "lcd":
                    print(single_data)
                    add_point("LCD", single_data)
                case "dht_1":
                    add_point_dht("DHT_1", single_data)
                case "dht_2":
                    add_point_dht("DHT_2", single_data)
                case "dht_3":
                    add_point_dht("DHT_3", single_data)
                case "gyroscope":
                    measurment_time = datetime.fromtimestamp(single_data['timestamp'], tz=timezone.utc)
                    point = Point("GYROSCOPE") \
                    .tag("name", single_data["name"]) \
                    .field("simulated", single_data["simulated"]) \
                    .field("rotation", single_data["rotation"])\
                    .field("acceleration", single_data["acceleration"])\
                    .time(measurment_time)
            
                    write_api.write(bucket="moj_bucket", record=point, org="moja_org")
                
                case "4sd":
                    print(single_data)
                    add_point("4SD", single_data)
                    
                case "people":
                    print(single_data["num_people"])
                    system_status_storage["num_people"] = single_data["num_people"]
                    
    elif type(payload) == dict:
        name = payload["name"]
        match name:
            case "dms":
                system_status_storage["security_system_state"] = payload["value"]
                
                measurment_time = datetime.fromtimestamp(payload['timestamp'], tz=timezone.utc)
                point = Point("DMS") \
                .tag("name", payload["name"]) \
                .field("simulated", payload["simulated"]) \
                .field("value", payload["value"])\
                .field("attempt", payload["attempt"])\
                .time(measurment_time)
            
                write_api.write(bucket="moj_bucket", record=point, org="moja_org")
                
            case "alarm":
                print(payload)
                system_status_storage["alarm_state"] = payload["value"]
                
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

def add_point_dht(measurment_name, single_data):
    measurment_time = datetime.fromtimestamp(single_data['timestamp'], tz=timezone.utc)
    point = Point(measurment_name) \
    .tag("name", single_data["name"]) \
    .field("simulated", single_data["simulated"]) \
    .field("temperature", single_data["temperature"])\
    .field("humidity", single_data["humidity"])\
    .time(measurment_time)

    write_api.write(bucket="moj_bucket", record=point, org="moja_org")
    

app = Flask(__name__)
CORS(app)

@app.route('/dms_input', methods=['POST']) #GADJAM http://localhost:5050/ime_rute iz Angulara
def handle_dms_input(): # Promenjeno ime ovde
    global client
    try:
        data = request.get_json()
        client.publish("commands/dms", json.dumps(data))
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/set_rgb', methods=['POST']) #GADJAM http://localhost:5050/ime_rute iz Angulara
def handle_rgb_input(): # Promenjeno ime ovde
    global client
    try:
        data = request.get_json()
        client.publish("commands/rgb", json.dumps(data))
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/start_kitchen_timer', methods=['POST']) #GADJAM http://localhost:5050/ime_rute iz Angulara
def handle_start_kitchen_timer(): # Promenjeno ime ovde
    global client
    try:
        data = request.get_json()
        client.publish("commands/start_kitchen_timer", json.dumps(data))
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
@app.route('/add_to_kitchen_timer', methods=['POST']) #GADJAM http://localhost:5050/ime_rute iz Angulara
def handle_add_to_kitchen_timer(): # Promenjeno ime ovde
    global client
    try:
        data = request.get_json()
        client.publish("commands/add_to_kitchen_timer", json.dumps(data))
        return jsonify({"status": "success"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


@app.route('/system_status', methods=['GET']) #GADJAM http://localhost:5050/ime_rute iz Angulara
def handle_system_status(): # Promenjeno ime ovde
    global client
    try:
        return jsonify(system_status_storage)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})


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
    client.connect("localhost", 1883, 60) #PROMENI NA IP UCIONICE

    # client.loop_forever()
    client.loop_start() # Pokreće MQTT u pozadinskom thread-u
    
    app.run(host="0.0.0.0", port=5050, debug=False)
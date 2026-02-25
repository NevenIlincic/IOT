from flask import Flask, jsonify, request
from flask_cors import CORS
import paho.mqtt.client as mqtt
import threading
import json
from datetime import datetime, timezone
import time

from settings import load_settings
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.client.write_api import WritePrecision

import paho.mqtt.client as mqtt

import paho.mqtt.subscribe as subscribe

from classes.alarm import Alarm
from classes.security_sistem import SecuritySystem

from enums import Attempt, State, AlarmState

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

alarm: Alarm = None
security_system: SecuritySystem = None

dht_lcd_shared_dict = {
    "dht_1": [20,20], # 1. Temperature, 2. Vlaznost
    "dht_2": [15,15],
    "dht_3": [10,10]
}


def on_connect(client, userdata, flags, rc):
    client.subscribe("devices")
    client.subscribe("people_in_system")
    client.subscribe("commands/add_people")
    client.subscribe("commands/subtract_people")
    client.subscribe("commands/dms")
    client.subscribe("commands/ds")
    client.subscribe("commands/alarm")
    client.subscribe("commands/btn")
    client.subscribe("commands/4sd")
    client.subscribe("commands/dht")

def on_message(client, userdata, msg):
    global alarm, security_system, system_status_storage, dht_lcd_shared_dict
    #print(msg.topic+" "+msg.payload.decode("utf-8"))
    topic = msg.topic
    payload = json.loads(msg.payload.decode("utf-8"))
    
    settings = userdata.get("settings")
    
    match topic:
        case "devices":
            handle_devices_messages(payload)
        case "commands/subtract_people":
            value = payload.get("subtract")
            print(system_status_storage)
            if system_status_storage["num_people"] != 0:
                system_status_storage["num_people"] -= value
            else:
                alarm.turn_on()  
        case "commands/add_people":
            value = payload.get("add")
            system_status_storage["num_people"] += value
            print(system_status_storage)
        case "commands/dms":
            success = Attempt.SUCCESS
            value = payload.get("password")
            if settings["DMS"]["password"] == value:
                if security_system.value == State.OFF:
                    if alarm.value == AlarmState.ACTIVE:
                        alarm.turn_off()
                    else:
                        time.sleep(10)
                        security_system.value = State.ON
                else:
                    if alarm.value == AlarmState.ACTIVE:
                        alarm.turn_off()
                    security_system.value = State.OFF
            else:
                success = Attempt.FAIL
                
            value = "SYSTEM ACTIVE" if security_system.value == State.ON else "SYSTEM NOT ACTIVE"
            
            data_to_send = {
                            "name": settings["DMS"]["name"],
                            "value": value,
                            "attempt": success.name,
                            "simulated": True,
                            "timestamp": time.time()
                        }
            
            system_status_storage["security_system_state"] = value
            
            client.publish(settings["topic"], json.dumps(data_to_send))
        case "commands/ds":
            ds_settings = None
            ds_name = payload.get("name")
            if ds_name == "ds_1":
                ds_settings = settings["DS1"]
            else:
                ds_settings = settings["DS2"]
            
            value = payload.get("ds_value")
            if security_system.value == State.OFF:
                if value == "CLOSED":
                    if ds_settings["start_time"]:
                        if alarm.value == AlarmState.ACTIVE and (time.time() - ds_settings["start_time"] > 5):
                            alarm.turn_off()

                    ds_settings["start_time"] = None
                else:
                    if ds_settings["start_time"] is None:
                        ds_settings["start_time"] = time.time()
                    else:
                        if time.time() - ds_settings["start_time"] > 5:
                            alarm.turn_on()
            else:
                if value == "OPEN":
                    ds_settings["start_time"] = None
                    alarm.turn_on()
                    
        case "commands/alarm":
            action = payload.get("action")
            if action == "ON":
                alarm.turn_on()
                
        case "commands/btn":
            data = {
                "seconds_to_add": 10
            }
            client.publish("commands/add_to_kitchen_timer", json.dumps(data))
        
        case "commands/dht":
            name = payload.get("name")
            temperature_and_humidity = payload.get("values")
            dht_lcd_shared_dict[name] = temperature_and_humidity
            

def handle_devices_messages(payload):
    if type(payload) == list:
        for single_data in payload:
            name = single_data["name"]
            
            match name:
                case "dpir_1":
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
                    add_point("DS_1", single_data)
                    
                    
                case "ds_2":
                    add_point("DS_2", single_data)
                case "btn":
                    add_point("BTN", single_data)
                        
                case "dl":
                    add_point("DL", single_data)
                
                case "db":
                    add_point("DB", single_data)
                
                case "lcd":
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
                    add_point("4SD", single_data)
                    
                case "people":
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


def run_lcd_thread(mqtt_client, lcd_settings):
    i = 0
    while True:
        current_dht = "dht_"+ str(i + 1)
        temp_string = ""
        humidity_string = ""
        if current_dht == "dht_1":    
            temp_string = 'Bedroom T: ' + str(dht_lcd_shared_dict[current_dht][0])+ "°C"'\n'
            humidity_string = 'Bedroom H: ' + str(dht_lcd_shared_dict[current_dht][1])+ "%" 
        elif current_dht == "dht_2":
            temp_string = 'Master T: ' + str(dht_lcd_shared_dict[current_dht][0])+ "°C"'\n'
            humidity_string = 'Master H: ' + str(dht_lcd_shared_dict[current_dht][1])+ "%" 
        else:
            temp_string = 'Kitchen T: ' + str(dht_lcd_shared_dict[current_dht][0])+ "°C"'\n'
            humidity_string = 'Kitchen H: ' + str(dht_lcd_shared_dict[current_dht][1])+ "%" 
            
        data = {
            "temp_string": temp_string,
            "humidity_string": humidity_string
        }
        mqtt_client.publish("commands/lcd", json.dumps(data))
        time.sleep(lcd_settings["delay"]) 
        i = (i+1) % 3

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
    
    
    alarm = Alarm(client, settings["ALARM"])
    security_system = SecuritySystem()

    # client.loop_forever()
    client.loop_start() # Pokreće MQTT u pozadinskom thread-u
    
    lcd_thread_thread = threading.Thread(target=run_lcd_thread, args=(client, settings["LCD"]), daemon=True)
    lcd_thread_thread.start()
    
    app.run(host="0.0.0.0", port=5050, debug=False)
    

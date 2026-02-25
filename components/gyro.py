from simulators.gyro import run_gyro_simulator
import threading
import time
import json

def gyro_callback(mqtt_client, gyro_settings, data_lock, batch, rotation, activity, stop_event):
    payload = {
        "name": gyro_settings["name"],
        "rotation": rotation,
        "acceleration": activity,
        "simulated": gyro_settings["simulated"],
        "timestamp": time.time()
    }
    
    if abs(gyro_settings["last_acceleration_value"] - activity) > 80 or abs(gyro_settings["last_rotation_value"] - rotation) > 50 :
        mqtt_client.publish("commands/alarm", json.dumps({"action": "ON"}))

    
    gyro_settings["last_acceleration_value"] = activity
    gyro_settings["last_rotation_value"] = rotation
    
    with data_lock:
        batch.append(payload)
        
    if stop_event.is_set():
        return



def run_gyro(mqtt_client, settings, threads, stop_event, data_lock, batch):
        if settings['simulated']:
            print("Starting GYRO sumilator")
            gyro_thread = threading.Thread(target = run_gyro_simulator, args=(mqtt_client,settings, data_lock, batch, gyro_callback, stop_event))
            gyro_thread.start()
            threads.append(gyro_thread)
            print("GYRO sumilator started")
        else:
            from sensors.gyroscope.gyro import run_gyro_loop
            print("Starting GYRO loop")
            dht1_thread = threading.Thread(target=run_gyro_loop, args=(mqtt_client, settings, data_lock, batch, gyro_callback, stop_event))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("GYRO loop started")

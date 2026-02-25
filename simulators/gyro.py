import random
import time
import math

def generate_values():
    while True:
        base_noise = random.uniform(0.1, 0.8)
        
        if random.random() > 0.95:
            activity = random.uniform(50.0, 150.0)
        else:
            activity = base_noise
            
        rotation = random.uniform(0.1, 0.5)

        if random.random() > 0.98:
            rotation = random.uniform(30.0, 150.0)
            
        yield activity, rotation

def run_gyro_simulator(mqtt_client, gyro_settings, data_lock, batch, callback, stop_event):
    for activity, rotation in generate_values():
        callback(mqtt_client, gyro_settings, data_lock, batch, rotation, activity, stop_event)
        
        time.sleep(gyro_settings["delay"])
        if stop_event.is_set():
            break
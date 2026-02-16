
from simulators.dus1 import run_dus_simulator
import threading
import time
import json

def rgb_callback(mqtt_client, rgb_settings, stop_event, value):
    payload = {
            "name": rgb_settings["name"],
            "value": value.name,
            "simulated": rgb_settings["simulated"],
            "timestamp": time.time()
    }
    
    mqtt_client.publish(rgb_settings["topic"], json.dumps(payload))

def run_rgb(mqtt_client, rgb_settings, threads, stop_event):
        if rgb_settings['simulated']:
            print("Starting dus simulator")
            # dus1_thread = threading.Thread(target = run_dus_simulator, args=(dus_settings, data_lock, batch, dus_callback, stop_event), daemon=True)
            # dus1_thread.start()
            # threads.append(dus1_thread)
            # print("Dus simulator started")
        else:
            from sensors.rgb import run_ir_loop, RGB 
            print("Starting RGB loop")
            rgb = RGB(rgb_settings)
            rgb_thread = threading.Thread(target=run_ir_loop, args=(rgb, mqtt_client, rgb_callback, stop_event))
            rgb_thread.start()
            threads.append(rgb_thread)
            print("IR loop started")

import time
import random
from enum import Enum
import json


class Attempt(Enum):
    SUCCESS = 1
    FAIL = 0

def toggle_locked(mqtt_client, settings, password):
    string_to_return = ""
    success = Attempt.SUCCESS
    if settings["password"] == password:
        settings['locked'] = not settings['locked']
        if settings['locked']:
            string_to_return = "Door Locked!"
        else:
            string_to_return = "Door Unlocked!"
    else:
        success = Attempt.FAIL
        string_to_return = "Wrong password!"
        
    value = "LOCKED" if settings["locked"] else "UNLOCKED"
    
    data_to_send = {
                    "name": settings["name"],
                    "value": value,
                    "attempt": success.name,
                    "simulated": True,
                    "timestamp": time.time()
                } 
    print(value)
    mqtt_client.publish(settings["topic"], json.dumps(data_to_send))
    # return settings, string_to_return

def generate_values(settings):
    while True:
        yield settings["locked"]
      

def run_dms_simulator(settings, callback, stop_event):
    for state in generate_values(settings):
        callback(state, "simulated")
        time.sleep(settings["delay"])  # Delay between readings (adjust as needed)
        if stop_event.is_set():
            break
              
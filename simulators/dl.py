import time
import random
from enum import Enum
import json


class DoorLightState(Enum):
    ON = 1
    OFF = 0


state = DoorLightState.OFF

def toggle_light(mqtt_client, settings):
    global state
    string_to_return = ""
    if state == DoorLightState.OFF:
        state = DoorLightState.ON
        string_to_return = "Light ON!"
    else:
        state = DoorLightState.OFF
        string_to_return = "Light OFF!"
    
    data_to_send = {
                "name": settings["name"],
                "value": string_to_return,
                "simulated": True,
                "timestamp": time.time()
            }
    
    print(string_to_return)
    mqtt_client.publish(settings["topic"], json.dumps(data_to_send))
    # return string_to_return

def generate_values():
    while True:
        yield state
      

def run_dl_simulator(delay, callback, stop_event):
    for state in generate_values():
        callback(state, "simulated")
        time.sleep(delay)  # Delay between readings (adjust as needed)
        if stop_event.is_set():
            break
              
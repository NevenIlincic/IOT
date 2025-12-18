import time
import random
from enum import Enum


class DoorLightState(Enum):
    ON = 1
    OFF = 0


state = DoorLightState.OFF

def toggle_light():
    global state
    string_to_return = ""
    if state == DoorLightState.OFF:
        state = DoorLightState.ON
        string_to_return = "Light ON!"
    else:
        state = DoorLightState.OFF
        string_to_return = "Light OFF!"
        
    return string_to_return

def generate_values():
    while True:
        yield state
      

def run_dl_simulator(delay, callback, stop_event):
    for state in generate_values():
        callback(state, "simulated")
        time.sleep(delay)  # Delay between readings (adjust as needed)
        if stop_event.is_set():
            break
              
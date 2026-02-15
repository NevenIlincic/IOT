import time
import random
from enum import Enum
import json
from enums import DoorLightState

state = DoorLightState.OFF

def toggle_light():
    global state
    state = DoorLightState.ON
    print("Light ON!")
    time.sleep(10)
    state = DoorLightState.OFF
    print("Light OFF!")

    
    
def generate_values():
    while True:
        yield state
      

def run_dl_simulator(settings, data_lock, batch, stop_event, callback):
    for state in generate_values():
        callback(settings, data_lock, batch, stop_event, state.name)
        time.sleep(settings["delay"])  # Delay between readings (adjust as needed)
        if stop_event.is_set():
            break
    
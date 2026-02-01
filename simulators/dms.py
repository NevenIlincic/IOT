import time
import random
from enum import Enum


class DoorMotion(Enum):
    ON = 1
    OFF = 0

def toggle_locked(settings, password):
    string_to_return = ""
    if settings["password"] == password:
        settings['locked'] = not settings['locked']
        if settings['locked']:
            string_to_return = "Door Locked!"
        else:
            string_to_return = "Door Unlocked!"
    else:
        string_to_return = "Wrong password!"
        
    return settings, string_to_return

def generate_values(settings):
    while True:
        yield settings["locked"]
      

def run_dms_simulator(settings, callback, stop_event):
    for state in generate_values(settings):
        callback(state, "simulated")
        time.sleep(settings["delay"])  # Delay between readings (adjust as needed)
        if stop_event.is_set():
            break
              
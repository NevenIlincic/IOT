import time
import random
from enum import Enum
import threading
import json
from enums import MotionDetected

def generate_values(initial_state = MotionDetected.NOT_DETECTED):
    state = initial_state
    while True:
        x = random.randint(0,2)
        if x == 0:
            state = MotionDetected.DETECTED
        else:
            state = MotionDetected.NOT_DETECTED
        yield state

def run_dpir_simulator(mqtt_client, settings, data_lock, batch, callback, stop_event, dl, dl_settings, dus_settings, dpir_dus_shared_dict, all_settings):
        for state in generate_values():
            callback(mqtt_client, settings, dl, dl_settings, data_lock, batch, stop_event, state, dus_settings, dpir_dus_shared_dict, all_settings)
            time.sleep(settings['delay']) 
            if stop_event.is_set():
                  break



import time
import random
from enum import Enum
import threading
import json
from enums import MotionDetected

def generate_values(initial_state = MotionDetected.NOT_DETECTED):
    state = initial_state
    while True:
        x = random.randint(0,10)
        if x == 0:
            state = MotionDetected.DETECTED
        else:
            state = MotionDetected.NOT_DETECTED
        yield state

def run_dpir_simulator(settings, data_lock, batch, callback, stop_event, dl, dl_settings):
        for state in generate_values():
            callback(settings, dl, dl_settings, data_lock, batch, stop_event, state)
            time.sleep(settings['delay']) 
            if stop_event.is_set():
                  break



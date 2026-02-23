import time
import random
from enum import Enum
import json
import threading
from enums import DoorState

last_state = DoorState.CLOSED

def generate_values(initial_state = DoorState.CLOSED, is_kitchen_button = True):
    global last_state
    state = initial_state
    while True:
        if is_kitchen_button:
            x = random.randint(0, 30)
        elif last_state == DoorState.CLOSED:
            x = random.randint(0,4)
        else:
            x = random.randint(-8, 2)
        if x <= 0:
            state = DoorState.OPEN
        else:
            state = DoorState.CLOSED
        yield state

def run_ds1_simulator(settings, data_lock, batch, stop_event, callback, alarm, security_system):
    for state in generate_values(is_kitchen_button=settings["kitchen_button"]):
        callback(settings, data_lock, batch, stop_event, state.name, alarm, security_system)
        time.sleep(settings['delay'])
        if stop_event.is_set():
            break
import time
import random
from enum import Enum
import json
import threading

class DoorState(Enum):
    OPEN = 1
    CLOSED = 0

def generate_values(initial_state = DoorState.CLOSED):
    state = initial_state
    while True:
        x = random.randint(0,10)
        if x == 0:
            state = DoorState.OPEN
        else:
            state = DoorState.CLOSED
        yield state

def run_ds1_simulator(settings, data_lock, batch, stop_event, callback):
    for state in generate_values():
        callback(settings, data_lock, batch, stop_event, state.name)
        time.sleep(settings['delay'])
        if stop_event.is_set():
            break
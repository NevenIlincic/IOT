import time
import random
from enum import Enum

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

def run_ds1_simulator(delay, callback, stop_event):
        for state in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(state, "simulated")
            if stop_event.is_set():
                  break
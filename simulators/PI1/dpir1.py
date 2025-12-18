import time
import random
from enum import Enum

class MotionDetected(Enum):
    DETECTED = 1
    NOT_DETECTED = 0

def generate_values(initial_state = MotionDetected.NOT_DETECTED):
    state = initial_state
    while True:
        x = random.randint(0,10)
        if x == 0:
            state = MotionDetected.DETECTED
        else:
            state = MotionDetected.NOT_DETECTED
        yield state

def run_dpir1_simulator(delay, callback, stop_event):
        for state in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(state, "simulated")
            if stop_event.is_set():
                  break
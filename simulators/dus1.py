import time
import random
import json
import threading

def generate_values(initial_distance = 50.0):
      distance = initial_distance
      while True:
            distance += float(random.randint(-150, 150 )) / 10
            if distance < 0:
                  distance = 0.0
            yield round(distance, 1)

      

def run_dus_simulator(settings, data_lock, batch, callback, stop_event, dpir_dus_shared_dict):
      for state in generate_values():
            callback(settings, data_lock, batch, stop_event, state, dpir_dus_shared_dict)
            time.sleep(settings['delay'])  # Delay between readings (adjust as needed)
            if stop_event.is_set():
                  break
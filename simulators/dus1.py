import time
import random

def generate_values(initial_distance = 50.0):
      distance = initial_distance
      while True:
            distance += float(random.randint(-150, 150 )) / 10
            if distance < 0:
                  distance = 0
            yield round(distance, 1)

      

def run_dus1_simulator(delay, callback, stop_event):
        for distance in generate_values():
            time.sleep(delay)  # Delay between readings (adjust as needed)
            callback(distance, "simulated")
            if stop_event.is_set():
                  break
              
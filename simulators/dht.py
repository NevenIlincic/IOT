import time
import random

def generate_values(initial_temp = 25, initial_humidity=20):
      temperature = initial_temp
      humidity = initial_humidity
      while True:
            temperature = temperature + random.randint(-1, 1)
            humidity = humidity + random.randint(-1, 1)
            if humidity < 0:
                  humidity = 0
            if humidity > 100:
                  humidity = 100
            yield humidity, temperature

      

def run_dht_simulator(dht_settings, data_lock, batch, callback, stop_event, dht_lcd_shared_dict):
      for h, t in generate_values():
            callback(dht_settings, data_lock, batch, t, h, stop_event, dht_lcd_shared_dict)
            time.sleep(dht_settings["delay"]) 
            if stop_event.is_set():
                  break
              
import time
import random

# def generate_values(initial_temp = 25, initial_humidity=20):
#       temperature = initial_temp
#       humidity = initial_humidity
#       while True:
#             temperature = temperature + random.randint(-1, 1)
#             humidity = humidity + random.randint(-1, 1)
#             if humidity < 0:
#                   humidity = 0
#             if humidity > 100:
#                   humidity = 100
#             yield humidity, temperature

      

def run_lcd_simulator(lcd_settings, data_lock, batch, callback, stop_event, dht_lcd_shared_dict):
    while True:
        current_dht = "dht"
        temp_string = 'Bedroom temp: ' + str(dht_lcd_shared_dict[current_dht][0])+ "°C"'\n'
        humidity_string = 'Bedroom hum: ' + str(dht_lcd_shared_dict[current_dht][1])+ "%" 
        callback(lcd_settings, data_lock, batch, temp_string, humidity_string, stop_event)
        time.sleep(lcd_settings["delay"]) 
        
        if stop_event.is_set():
                break
              
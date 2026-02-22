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
    i = 0
    while True:
        current_dht = "dht_"+ str(i + 1)
        temp_string = ""
        humidity_string = ""
        if current_dht == "dht_1":    
            temp_string = 'Bedroom T: ' + str(dht_lcd_shared_dict[current_dht][0])+ "°C"'\n'
            humidity_string = 'Bedroom H: ' + str(dht_lcd_shared_dict[current_dht][1])+ "%" 
        elif current_dht == "dht_2":
            temp_string = 'Master T: ' + str(dht_lcd_shared_dict[current_dht][0])+ "°C"'\n'
            humidity_string = 'Master T: ' + str(dht_lcd_shared_dict[current_dht][1])+ "%" 
        else:
            temp_string = 'Kitchen T: ' + str(dht_lcd_shared_dict[current_dht][0])+ "°C"'\n'
            humidity_string = 'Kitchen H: ' + str(dht_lcd_shared_dict[current_dht][1])+ "%" 
            
        callback(lcd_settings, data_lock, batch, temp_string, humidity_string, stop_event)
        time.sleep(lcd_settings["delay"]) 
        i = (i+1) % 3
        if stop_event.is_set():
                break
              
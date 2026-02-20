
from sensors.lcd.LCD1602 import run_lcd_loop
from simulators.lcd import run_lcd_simulator
import threading
import time

def lcd_callback(lcd_settings, data_lock, batch, temperature, humidity, stop_event):
    
    value = temperature + humidity
    payload = {
        "name": lcd_settings["name"],
        "value": value,
        "simulated": lcd_settings["simulated"],
        "timestamp": time.time()
    }
    
    with data_lock:
        batch.append(payload)
        
    if stop_event.is_set():
        return



def run_lcd(settings, threads, stop_event, data_lock, batch, dht_lcd_shared_dict):
        if settings['simulated']:
            print("Starting LCD sumilator")
            gyro_thread = threading.Thread(target = run_lcd_simulator, args=(settings, data_lock, batch, lcd_callback, stop_event, dht_lcd_shared_dict), daemon=True)
            gyro_thread.start()
            threads.append(gyro_thread)
            print("LCD sumilator started")
        else:
            print("Starting LCD loop")
            dht1_thread = threading.Thread(target=run_lcd_loop, args=(settings, lcd_callback, data_lock, batch, stop_event, dht_lcd_shared_dict))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("LCD loop started")

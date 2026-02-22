
import threading
import time

def sd_callback(sd_settings, data_lock, batch, stop_event):
    seconds = sd_settings["seconds"]
    minutes = seconds // 60
    seconds = seconds - (minutes*60)

    if minutes >= 10:
        minutes = str(minutes)
    else:
        minutes = "0" + str(minutes)
    
    if seconds >= 10:
        seconds = str(seconds)
    else:
        seconds = "0" + str(seconds)
    
    value = minutes + ":" + seconds
    
    payload = {
        "name": sd_settings["name"],
        "value": value,
        "simulated": sd_settings["simulated"],
        "timestamp": time.time()
    }
    
    with data_lock:
        batch.append(payload)
        
    if stop_event.is_set():
        return



# def run_lcd(settings, threads, stop_event, data_lock, batch, dht_lcd_shared_dict):
#         if settings['simulated']:
#             print("Starting LCD sumilator")
#             gyro_thread = threading.Thread(target = run_lcd_simulator, args=(settings, data_lock, batch, lcd_callback, stop_event, dht_lcd_shared_dict), daemon=True)
#             gyro_thread.start()
#             threads.append(gyro_thread)
#             print("LCD sumilator started")
#         else:
#             pass
            # from sensors.lcd.LCD1602 import run_lcd_loop
            # print("Starting LCD loop")
            # dht1_thread = threading.Thread(target=run_lcd_loop, args=(settings, lcd_callback, data_lock, batch, stop_event, dht_lcd_shared_dict))
            # dht1_thread.start()
            # threads.append(dht1_thread)
            # print("LCD loop started")

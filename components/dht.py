

from simulators.dht import run_dht_simulator
import threading
import time

def dht_callback(dht_settings, data_lock, batch, temperature, humidity, stop_event, dht_lcd_shared_dict ):
    
    dht_lcd_shared_dict[dht_settings["name"]] = [temperature, humidity]
    
    payload = {
        "name": dht_settings["name"],
        "temperature": temperature,
        "humidity": humidity,
        "simulated": dht_settings["simulated"],
        "timestamp": time.time()
    }
    
    with data_lock:
        batch.append(payload)
        
    if stop_event.is_set():
        return



def run_dht(settings, threads, stop_event, data_lock, batch, dht_lcd_shared_dict):
        if settings['simulated']:
            print("Starting DHT sumilator")
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(settings, data_lock, batch, dht_callback, stop_event, dht_lcd_shared_dict))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("DHT sumilator started")
        else:
            from sensors.dht import run_dht_loop, DHT
            print("Starting DHT loop")
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(dht, data_lock, batch, dht_callback, stop_event, dht_lcd_shared_dict))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("DHT loop started")

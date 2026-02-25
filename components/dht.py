

from simulators.dht import run_dht_simulator
import threading
import time
import json

def dht_callback(mqtt_client, dht_settings, data_lock, batch, temperature, humidity, stop_event):
    
    mqtt_client.publish("commands/dht", json.dumps(
        {
            "name": dht_settings["name"],
            "values": [temperature, humidity]
         }
        ))
    
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



def run_dht(mqtt_client, settings, threads, stop_event, data_lock, batch):
        if settings['simulated']:
            print("Starting DHT sumilator")
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(mqtt_client, settings, data_lock, batch, dht_callback, stop_event))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("DHT sumilator started")
        else:
            from sensors.dht import run_dht_loop, DHT
            print("Starting DHT loop")
            dht = DHT(settings['pin'])
            dht1_thread = threading.Thread(target=run_dht_loop, args=(mqtt_client, dht, data_lock, batch, dht_callback, stop_event))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("DHT loop started")

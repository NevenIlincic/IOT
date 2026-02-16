
from simulators.dus1 import run_dus_simulator
import threading
import time
import json

def dus_callback(dus_settings, data_lock, batch, stop_event, distance):
    payload = {
            "name": dus_settings["name"],
            "value": distance,
            "simulated": dus_settings["simulated"],
            "timestamp": time.time()
    }
    
    with data_lock:
            batch.append(payload)
            
    if stop_event.is_set():
        return

def run_dus(dus_settings, threads, stop_event, batch, data_lock):
        if dus_settings['simulated']:
            print("Starting dus simulator")
            dus1_thread = threading.Thread(target = run_dus_simulator, args=(dus_settings, data_lock, batch, dus_callback, stop_event), daemon=True)
            dus1_thread.start()
            threads.append(dus1_thread)
            print("Dus simulator started")
        else:
            from sensors.dus import run_dus_loop, DUS 
            print("Starting DUS loop")
            dus = DUS(dus_settings)
            dus1_thread = threading.Thread(target=run_dus_loop, args=(dus, 2, dus_callback, stop_event))
            dus1_thread.start()
            threads.append(dus1_thread)
            print("DUS loop started")

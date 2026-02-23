import threading
import time
import json
from simulators.db import run_db_simulator

def db_callback(settings, data_lock, batch, stop_event, value):
    payload = {
        "name": settings["name"],
        "value": value,
        "simulated": settings["simulated"],
        "timestamp": time.time()
    }
    
    with data_lock:
        batch.append(payload)
        
    if stop_event.is_set():
        return


def run_db(db, settings, batch, data_lock, threads, stop_event):
    if settings['simulated']:
        print("Starting DB simulator")
        pass
        # dht1_thread = threading.Thread(target = run_db_simulator, args=(settings, data_lock, batch, stop_event, db_callback), daemon=True)
        # dht1_thread.start()
        # threads.append(dht1_thread)
        # print("DB sumilator started")
    else:
        from sensors.db import run_db_loop
        ds_thread = threading.Thread(target=run_db_loop, args=(db, settings, data_lock, batch, stop_event, db_callback), daemon=True)
        ds_thread.start()
        threads.append(ds_thread)
        print("DB loop started")
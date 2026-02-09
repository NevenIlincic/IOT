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
        print("Starting dht1 sumilator")
        dht1_thread = threading.Thread(target = run_db_simulator, args=(settings, data_lock, batch, stop_event, db_callback))
        dht1_thread.start()
        threads.append(dht1_thread)
        print("Dht1 sumilator started")
    else:
        from sensors.db import run_db_loop, DB
        print("Starting DB loop")
        #db = DB(settings, batch)
        ds_thread = threading.Thread(target=run_db_loop, args=(db, settings, data_lock, batch, stop_event, db_callback))
        ds_thread.start()
        threads.append(ds_thread)
        print("DB loop started")

from simulators.ds1 import run_ds1_simulator
import threading
import time
import random
from enum import Enum
from enums import AlarmState

def ds_callback(settings, data_lock, batch, stop_event, value, alarm):
    payload = {
        "name": settings["name"],
        "value": value,
        "simulated": settings["simulated"],
        "timestamp": time.time()
    }
    
    if settings["name"] == "ds_1" or settings["name"] == "ds_2":
        if value == "CLOSED":
            if settings["start_time"]:
                if alarm.value == AlarmState.ACTIVE and (time.time() - settings["start_time"] > 5):
                    alarm.turn_off()

            settings["start_time"] = None
        else:
            if settings["start_time"] is None:
                settings["start_time"] = time.time()
            else:
                if time.time() - settings["start_time"] > 5:
                    alarm.turn_on()
                
    
    with data_lock:
        batch.append(payload)
        
    if stop_event.is_set():
        return
    # t = time.localtime()
    # s = "="*20
    # s +=  "\nDevice: Door Sensor 1\n"
    # s += f"Timestamp: {time.strftime('%H:%M:%S', t)}\n"
    # s += f"Code: {code}\n"
    # s += f"State: {state.name}"
    # print(s)





def run_ds(settings, batch, data_lock, threads, stop_event, alarm, sd_settings=None):
        if settings['simulated']:
            print("Starting" + settings["name"] + " simulator")
            ds1_thread = threading.Thread(target = run_ds1_simulator, args=(settings, data_lock, batch, stop_event, ds_callback, alarm ), daemon=True)
            ds1_thread.start()
            threads.append(ds1_thread)
            print(settings["name"] + " simulator started")
        else:
            from sensors.ds import run_ds_loop, DS
            print("Starting DS loop")
            ds = DS(settings, batch, sd_settings)
            ds_thread = threading.Thread(target=run_ds_loop, args=(ds, settings, data_lock, batch, stop_event, ds_callback, alarm), daemon=True)
            ds_thread.start()
            threads.append(ds_thread)
            print("DS loop started")

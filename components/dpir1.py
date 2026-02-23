
from simulators.dpir1 import run_dpir_simulator
from components.dl import dl_callback
import threading
import time
from enums import DoorLightState
from enums import MotionDetected

def dpir_callback(dpir_settings, dl, dl_settings, data_lock, batch, stop_event, value):
    payload = {
            "name": dpir_settings["name"],
            "value": value.name,
            "simulated": dpir_settings["simulated"],
            "timestamp": time.time()
    }
    
    if dpir_settings["name"] == "dpir_1":
        if dl:
            if value == MotionDetected.DETECTED:
                dl.toggle_light(data_lock, stop_event, dl_callback)
                
        else:
            if value == MotionDetected.DETECTED:
                dl_thread = threading.Thread(target = run_simulated_dl_thread, args=(dl_settings, data_lock, batch, stop_event), daemon=True)
                dl_thread.start()
    
    with data_lock:
            batch.append(payload)
            
    if stop_event.is_set():
        return


def run_dpir(settings, threads, stop_event, batch, data_lock, dl, dl_settings):
    if settings['simulated']:
        print("Starting DPIR simulator")
        dpir_thread = threading.Thread(target = run_dpir_simulator, args=(settings, data_lock, batch, dpir_callback, stop_event, dl, dl_settings), daemon=True)
        dpir_thread.start()
        threads.append(dpir_thread)
        print("DPIR simulator started")
    else:
        from sensors.dpir import run_dpir_loop, DPIR
        print("Starting DPIR loop")
        dpir = DPIR(settings)
        dpir_thread = threading.Thread(target=run_dpir_loop, args=(dpir, settings, data_lock, batch, stop_event, dpir_callback, dl, dl_settings), daemon=True)
        dpir_thread.start()
        threads.append(dpir_thread)
        print("DPIR loop started")

def run_simulated_dl_thread(dl_settings, data_lock, batch, stop_event):
    dl_callback(dl_settings, data_lock, batch, stop_event, DoorLightState.ON.name)
    time.sleep(10)
    dl_callback(dl_settings, data_lock, batch, stop_event, DoorLightState.OFF.name)
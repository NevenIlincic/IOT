
from simulators.dpir1 import run_dpir_simulator
import threading
import time

def dpir_callback(dpir_settings, data_lock, batch, stop_event, value):
    payload = {
            "name": dpir_settings["name"],
            "value": value.name,
            "simulated": dpir_settings["simulated"],
            "timestamp": time.time()
    }
    
    with data_lock:
            batch.append(payload)
            
    if stop_event.is_set():
        return


def run_dpir(settings, threads, stop_event, batch, data_lock):
    if settings['simulated']:
        print("Starting DPIR simulator")
        dpir_thread = threading.Thread(target = run_dpir_simulator, args=(settings, data_lock, batch, dpir_callback, stop_event), daemon=True)
        dpir_thread.start()
        threads.append(dpir_thread)
        print("DPIR simulator started")
    else:
        from sensors.dpir import run_dpir_loop, DPIR
        print("Starting DPIR loop")
        dpir = DPIR(settings)
        dpir_thread = threading.Thread(target=run_dpir_loop, args=(dpir, settings, data_lock, batch, stop_event, dpir_callback), daemon=True)
        dpir_thread.start()
        threads.append(dpir_thread)
        print("DPIR loop started")

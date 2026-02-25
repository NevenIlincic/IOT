import time
import threading
from simulators.dl import run_dl_simulator

def dl_callback(settings, data_lock, batch, stop_event, value):
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
    
    # t = time.localtime()
    # s = "="*20
    # s +=  "\nDevice: Door Light 1\n"
    # s += f"Timestamp: {time.strftime('%H:%M:%S', t)}\n"
    # s += f"Code: {code}\n"
    # s += f"State: {state.name}"
    # print(s)


def run_dl(dl, settings, batch, data_lock, threads, stop_event):
    if settings['simulated']:
        print("Starting dl simulator")
        # dl1_thread = threading.Thread(target = run_dl_simulator, args=(settings, data_lock, batch, stop_event, dl_callback), daemon=True)
        # dl1_thread.start()
        # threads.append(dl1_thread)
        # print("Dl simulator started")
    else:
        from sensors.dl import run_dl_loop, DL
        print("Starting DL loop")
        # #dl = DB(settings, batch)
        # ds_thread = threading.Thread(target=run_dl_loop, args=(dl, settings, data_lock, batch, stop_event, dl_callback), daemon=True)
        # ds_thread.start()
        # threads.append(ds_thread)
        # print("DL loop started")
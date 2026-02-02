import time
import threading
from simulators.dms import run_dms_simulator

def dms_callback(locked, code):
    t = time.localtime()
    s = "="*20
    s +=  "\nDevice: Door Membrane Switch\n"
    s += f"Timestamp: {time.strftime('%H:%M:%S', t)}\n"
    s += f"Code: {code}\n"
    if locked:
        s += f"Locked: Locked\n"
    else:
        s += f"Locked: Unlocked\n"
    print(s)


def run_dms(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting DMS simulator")
            dms_thread = threading.Thread(target = run_dms_simulator, args=(settings, dms_callback, stop_event), daemon=True)
            dms_thread.start()
            threads.append(dms_thread)
            print("DMS simulator started")
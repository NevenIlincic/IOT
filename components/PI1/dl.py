import time
import threading
from simulators.PI1.dl import run_dl_simulator

def dl1_callback(state, code):
    t = time.localtime()
    s = "="*20
    s +=  "\nDevice: Door Light 1\n"
    s += f"Timestamp: {time.strftime('%H:%M:%S', t)}\n"
    s += f"Code: {code}\n"
    s += f"State: {state.name}"
    print(s)


def run_dl1(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dl simulator")
            dl1_thread = threading.Thread(target = run_dl_simulator, args=(settings["delay"], dl1_callback, stop_event), daemon=True)
            dl1_thread.start()
            threads.append(dl1_thread)
            print("Dl simulator started")
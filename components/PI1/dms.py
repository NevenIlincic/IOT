import time
import threading
from simulators.PI1.dms import run_dms_simulator
from colorama import init

init(autoreset=True)

def dms_callback(locked, code):
    t = time.localtime()
    s = "="*20
    s +=  "\n\033[1;36mDevice: Door Membrane Switch\033[0m\n"
    s += f"Timestamp: {time.strftime('%H:%M:%S', t)}\n"
    s += f"Code: {code}\n"
    if locked:
        s += f"Locked: \033[1mLocked\033[0m"
    else:
        s += f"Locked: \033[1mUnlocked\033[0m"
    print(s)


def run_dms(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting DMS simulator")
            dms_thread = threading.Thread(target = run_dms_simulator, args=(settings, dms_callback, stop_event), daemon=True)
            dms_thread.start()
            threads.append(dms_thread)
            print("DMS simulator started")
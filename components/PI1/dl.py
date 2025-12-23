import time
import threading
from simulators.PI1.dl import run_dl_simulator
from colorama import init

init(autoreset=True)

def dl1_callback(state, code):
    t = time.localtime()
    s = "="*20
    s +=  "\n\033[1;31mDevice: Door Light 1\033[0m\n"
    s += f"Timestamp: {time.strftime('%H:%M:%S', t)}\n"
    s += f"Code: {code}\n"
    s += f"State: \033[1m{state.name}\033[0m"
    print(s)


def run_dl1(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dl simulator")
            dl1_thread = threading.Thread(target = run_dl_simulator, args=(settings["delay"], dl1_callback, stop_event), daemon=True)
            dl1_thread.start()
            threads.append(dl1_thread)
            print("Dl simulator started")
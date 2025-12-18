
from simulators.PI1.dpir1 import run_dpir1_simulator
import threading
import time

def dpir1_callback(state, code):
    t = time.localtime()
    s = "="*20
    s +=  "\nDevice: Door Motion Sensor 1\n"
    s += f"Timestamp: {time.strftime('%H:%M:%S', t)}\n"
    s += f"Code: {code}\n"
    s += f"Motion: {state.name}"
    print(s)


def run_dpir1(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dpir1 simulator")
            ds1_thread = threading.Thread(target = run_dpir1_simulator, args=(settings["delay"], dpir1_callback, stop_event))
            ds1_thread.start()
            threads.append(ds1_thread)
            print("Dpir1 simulator started")
        # else:
        #     from sensors.dht import run_dht_loop, DHT
        #     print("Starting dpir1 loop")
        #     dht = DHT(settings['pin'])
        #     ds1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dpir1_callback, stop_event))
        #     ds1_thread.start()
        #     threads.append(ds1_thread)
        #     print("Dpir loop started")

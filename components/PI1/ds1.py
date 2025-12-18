
from simulators.PI1.ds1 import run_ds1_simulator
import threading
import time

def ds1_callback(state, code):
    t = time.localtime()
    s = "="*20
    s +=  "\nDevice: Door Sensor 1\n"
    s += f"Timestamp: {time.strftime('%H:%M:%S', t)}\n"
    s += f"Code: {code}\n"
    s += f"State: {state.name}"
    print(s)


def run_ds1(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting ds1 simulator")
            ds1_thread = threading.Thread(target = run_ds1_simulator, args=(settings["delay"], ds1_callback, stop_event))
            ds1_thread.start()
            threads.append(ds1_thread)
            print("Ds1 simulator started")
        # else:
        #     from sensors.dht import run_dht_loop, DHT
        #     print("Starting dht1 loop")
        #     dht = DHT(settings['pin'])
        #     ds1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, ds1_callback, stop_event))
        #     ds1_thread.start()
        #     threads.append(ds1_thread)
        #     print("Dht1 loop started")

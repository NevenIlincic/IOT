
from simulators.PI1.dus1 import run_dus1_simulator
import threading
import time

def dus1_callback(distance, code):
    t = time.localtime()
    s = "="*20
    s += "\nDevice: Door Ultra Sonic Sensor 1\n"
    s += f"Timestamp: {time.strftime('%H:%M:%S', t)}\n"
    s += f"Code: {code}\n"
    s += f"Distance: {distance}cm"
    print(s)



def run_dus1(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dus1 simulator")
            dus1_thread = threading.Thread(target = run_dus1_simulator, args=(settings["delay"], dus1_callback, stop_event), daemon=True)
            dus1_thread.start()
            threads.append(dus1_thread)
            print("Dus1 simulator started")
        # else:
        #     from sensors.dht import run_dht_loop, DHT
        #     print("Starting dht1 loop")
        #     dht = DHT(settings['pin'])
        #     dus1_thread = threading.Thread(target=run_dht_loop, args=(dht, 2, dus1_callback, stop_event))
        #     dus1_thread.start()
        #     threads.append(dus1_thread)
        #     print("Dht1 loop started")

import threading
import time

def run_dht(settings, threads, stop_event):
        if settings['simulated']:
            print("Starting dht1 sumilator")
            dht1_thread = threading.Thread(target = run_dht_simulator, args=(2, dht_callback, stop_event))
            dht1_thread.start()
            threads.append(dht1_thread)
            print("Dht1 sumilator started")

import threading
from settings import load_settings
from components.dht import run_dht
from components.PI1.ds1 import run_ds1
from components.PI1.dus1 import run_dus1
from components.PI1.dpir1 import run_dpir1
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass


if __name__ == "__main__":
    print('Starting app')
    settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        # dht1_settings = settings['DHT1']
        ds1_settings = settings['DS1']
        dus1_settings = settings['DUS1']
        dpir1_settings = settings['DPIR1']
        # run_dht(dht1_settings, threads, stop_event)
        run_ds1(ds1_settings, threads, stop_event)
        run_dus1(dus1_settings, threads, stop_event)
        run_dpir1(dpir1_settings, threads, stop_event)
        # while True:
        #     time.sleep(1)

    except KeyboardInterrupt:
        print('Stopping app')
        for t in threads:
            stop_event.set()

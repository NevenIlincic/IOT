
import threading
from settings import load_settings

settings = load_settings()

smart_print_enabled = settings['PRINT']['activated']
if smart_print_enabled:
    try:
        import builtins
        from prompt_toolkit import print_formatted_text as safe_print
        builtins.print = safe_print
        print("Smart print is ENABLED")
    except ImportError:
        print("Warning: prompt_toolkit not found. Falling back to standard print.")
        smart_print_enabled = False

from components.dht import run_dht
from components.PI1.ds1 import run_ds1
from components.PI1.dus1 import run_dus1
from components.PI1.dpir1 import run_dpir1
from components.PI1.dl import run_dl1
from components.PI1.dms import run_dms

from cli import run_cli
import time

try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except:
    pass

#treba pip install prompt_toolkit prvo i virtuelno okruzenje da se instalira na RaspberryPI
if __name__ == "__main__":
    print('Starting app')
    #settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        # dht1_settings = settings['DHT1']
        ds1_settings = settings['DS1']
        dus1_settings = settings['DUS1']
        dpir1_settings = settings['DPIR1']
        dl1_settings = settings['DL']
        dms_settings = settings['DMS']
        # run_dht(dht1_settings, threads, stop_event)
        run_ds1(ds1_settings, threads, stop_event)
        run_dus1(dus1_settings, threads, stop_event)
        run_dpir1(dpir1_settings, threads, stop_event)
        run_dl1(dl1_settings, threads, stop_event)
        run_dms(dms_settings, threads, stop_event)
        
        cli_thread = threading.Thread(target = run_cli, args=(settings, stop_event), daemon=True)
        cli_thread.start()
        threads.append(cli_thread)

        while not stop_event.is_set():
            time.sleep(0.5)


    except KeyboardInterrupt:
        for t in threads:
            stop_event.set()

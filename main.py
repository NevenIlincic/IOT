
import threading
from settings import load_settings
import paho.mqtt.client as mqtt
import json

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
from components.ds1 import run_ds
from components.dus1 import run_dus
from components.dpir1 import run_dpir
from components.dl import run_dl
from components.dms import run_dms
from components.db import run_db
from components.dht import run_dht
# from components.gyro import run_gyro
from components.lcd import run_lcd
from components.ir import run_ir

# from sensors.db import DB
# from sensors.dl import DL
# from sensors.dms import DMS

from classes.alarm import Alarm
from classes.security_sistem import SecuritySystem

from cli import run_cli
import time

# try:
#     import RPi.GPIO as GPIO
#     GPIO.setmode(GPIO.BCM)
# except:
#     pass


def fill_batch(mqtt_client, batch, data_lock, settings):
    data_to_send = []
    while not stop_event.is_set():
        time.sleep(2)
        with data_lock:
            data_to_send = list(batch)
            batch.clear()
        
        if data_to_send:
            mqtt_client.publish(settings["topic"], json.dumps(data_to_send))
    
    with data_lock:
        if batch:
            mqtt_client.publish(settings["topic"], json.dumps(data_to_send))
            

#treba pip install prompt_toolkit prvo i virtuelno okruzenje da se instalira na RaspberryPI
if __name__ == "__main__":
    print('Starting app')
    batch = []
    data_lock = threading.Lock()
    #settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        mqtt_client = mqtt.Client()
        mqtt_client.connect("192.168.107.153", 1883, 60)
        mqtt_client.loop_start()
        
        dht1_settings = settings['DHT1']
        alarm_settings = settings["ALARM"]
        ds1_settings = settings['DS']
        dus_settings = settings['DUS']
        dpir_settings = settings['DPIR']
        dl_settings = settings['DL']
        dms_settings = settings['DMS']
        db_settings = settings["DB"]
        gyro_settings = settings["GYRO"]
        lcd_settings = settings["LCD"]
        ir_settings = settings["IR"]
        rgb_settings = settings["RGB"]
        # run_dht(dht1_settings, threads, stop_event)
        
        alarm = Alarm(mqtt_client, alarm_settings)
        security_system = SecuritySystem()
        
        dht_lct_shared_dict = {
            "dht": [20, 20] #1. Temperatura, 2. Humidity
        }
        #db = DB(db_settings, batch)
        # dl = DL(dl_settings, batch)
        
        #run_ds(ds1_settings, batch, data_lock, threads, stop_event)
        #run_dus(dus_settings, threads, stop_event, batch, data_lock)
       # run_dpir(dpir_settings, threads, stop_event, batch, data_lock)
        #run_db(db, db_settings, batch, data_lock, threads, stop_event)
        # run_dl(dl, dl_settings, batch, data_lock, threads, stop_event)
        #run_dms(mqtt_client, alarm, security_system, dms_settings, batch, data_lock, threads, stop_event)
        run_dht(dht1_settings, threads, stop_event, data_lock, batch, dht_lct_shared_dict)
        #run_gyro(gyro_settings, threads, stop_event, data_lock, batch)
        #run_lcd(lcd_settings, threads, stop_event, data_lock, batch, dht_lct_shared_dict)
        #run_ir(mqtt_client, ir_settings, threads, stop_event, rgb_settings)
        
        
        batch_thread =  threading.Thread(target=fill_batch, args=(mqtt_client, batch, data_lock, settings))
        batch_thread.start()
        threads.append(batch_thread)
        
        # run_dl1(dl1_settings, threads, stop_event)
        # run_dms(dms_settings, threads, stop_event)
        
        cli_thread = threading.Thread(target = run_cli, args=(mqtt_client,data_lock, batch, settings, stop_event, None, None, alarm, security_system), daemon=True)
        cli_thread.start()
        threads.append(cli_thread)

        while not stop_event.is_set():
            time.sleep(0.5)


    except KeyboardInterrupt:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        for t in threads:
            stop_event.set()


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
from components.gyro import run_gyro
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


from components.db import db_callback

from enums import Buzzing

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
            
def run_sd_counter(settings, data_lock, batch, stop_event):
    from components.sd import sd_callback
    sd_callback(settings["4SD"], data_lock, batch, stop_event)
    while True:
        settings["4SD"]["seconds"] -= 1
        print(settings["4SD"]["seconds"])
        sd_callback(settings["4SD"], data_lock, batch, stop_event)
        time.sleep(0.9)
        
        if settings["4SD"]["seconds"] == 0: 
            settings["4SD"]["blinking"] = True
            print("BLINKING!")
            break

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker")
    # client.subscribe("commands/buzzer")
    # client.subscribe("commands/dms")
    # client.subscribe("commands/rgb")
    client.subscribe("commands/start_kitchen_timer")
    client.subscribe("commands/add_to_kitchen_timer")

def on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        
        settings = userdata.get("settings")
        data_lock = userdata.get("data_lock")
        batch = userdata.get("batch")
        stop_event = userdata.get("stop_event")
        db = userdata.get("db")
        dl = userdata.get("dl")
            
        # elif msg.topic == "commands/dl":
        #     action = payload.get("action")
        #     if action == "ON":
        #         if not dl is None:
        #             dl.toggle_buzz(True)
        #         else:
        #             db_callback(settings["DB"], data_lock, batch, stop_event, Buzzing.BUZZING.name)
        #     else:
        #         if not db is None:
        #             db.toggle_buzz(False)
        #         else:
        #             db_callback(settings["DB"], data_lock, batch, stop_event, Buzzing.STOPPED.name)
            
        
        # if msg.topic == "commands/dms":
        #     typed_password = payload.get("password")
            
        #     alarm = userdata.get('alarm')
        #     security_system = userdata.get('security_system')
        #     dms_settings = userdata.get('settings')['DMS']
            
        #     # Sada pozivamo dms_callback koji se nalazi u tvojoj komponenti
        #     from components.dms import dms_callback
        #     print(f"Received DMS command from Flask. Password: {typed_password}")
            
        #     dms_callback(client, dms_settings, typed_password, alarm, security_system)
        # if msg.topic == "commands/rgb":
        #     selected_number = payload.get("selected_number")
            
        #     alarm = userdata.get('alarm')
        #     security_system = userdata.get('security_system')
        #     dms_settings = userdata.get('settings')['DMS']
        #     rgb = userdata.get("rgb")
            
        #     # Sada pozivamo dms_callback koji se nalazi u tvojoj komponenti
        #     from components.ir import ir_callback
        #     print(f"Received RGB command from Flask. Selected number: {selected_number}")
            
        #     ir_callback(client, settings["IR"], rgb, settings["RGB"], stop_event, selected_number)
        if msg.topic == "commands/start_kitchen_timer":
            total_seconds = payload.get("total_seconds")
            
            threads = userdata.get("threads")

            settings["4SD"]["seconds"] = total_seconds         
            sd_thread = threading.Thread(target = run_sd_counter, args=(settings, data_lock, batch, stop_event), daemon=True)
            sd_thread.start()
            threads.append(sd_thread)
            
        if msg.topic == "commands/add_to_kitchen_timer":
            seconds_to_add = payload.get("seconds_to_add")
            if settings["4SD"]["seconds"] > 0:
                settings["4SD"]["seconds"] += seconds_to_add
            elif settings["4SD"]["blinking"]:
                settings["4SD"]["blinking"] = False
                print("Stopped BLINKING")
        
    except Exception as e:
        print(f"Error in on_message: {e}")

    

#treba pip install prompt_toolkit prvo i virtuelno okruzenje da se instalira na RaspberryPI
if __name__ == "__main__":
    print('Starting app')
    batch = []
    data_lock = threading.Lock()
    #settings = load_settings()
    threads = []
    stop_event = threading.Event()
    try:
        security_system = SecuritySystem()
        
        mqtt_userdata = {
            "settings": settings,
            "security_system": security_system,
            "batch": batch,
            "data_lock": data_lock,
            "stop_event": stop_event
        }
        
        mqtt_client = mqtt.Client(userdata=mqtt_userdata)
        
        mqtt_client.on_connect = on_connect
        mqtt_client.on_message = on_message
        
        mqtt_client.connect("localhost", 1883, 60) #192.168.107.153
        mqtt_client.loop_start()
        
        # dht1_settings = settings['DHT1']
        # dht2_settings = settings['DHT2']
        dht3_settings = settings['DHT3']
        
        #ds1_settings = settings['DS1']
        ds2_settings = settings['DS2']
        btn_settings = settings["BTN"]
        
        alarm_settings = settings["ALARM"]
        
        #dus1_settings = settings['DUS1']
        dus2_settings = settings['DUS2']
        
        #dpir1_settings = settings['DPIR1']
        dpir2_settings = settings['DPIR2']
        # dpir3_settings = settings['DPIR3']
        
        
        dl_settings = settings['DL']
       # dms_settings = settings['DMS']
      #  db_settings = settings["DB"]
        gyro_settings = settings["GYRO"]
        # lcd_settings = settings["LCD"]
        # ir_settings = settings["IR"]
        # rgb_settings = settings["RGB"]
        sd_settings = settings["4SD"]
        # run_dht(dht1_settings, threads, stop_event)
        
        
        dht_lct_shared_dict = {
            "dht_1": [20, 20],
            "dht_2": [15,15],
            "dht_3": [10,10]#1. Temperatura, 2. Humidity
        }
        
        dpir_dus_shared_dict = {
            #"dus_1": [dus1_settings["start_distance"], dus1_settings["end_distance"], dus1_settings["last_distance"]],
            "dus_2": [dus2_settings["start_distance"], dus2_settings["end_distance"], dus2_settings["last_distance"]]
        }
        
        time_counter = 0
        is_blinking = False
        
        db = None
        # if not db_settings["simulated"]:
        #     from sensors.db import DB
        #     db = DB(db_settings, batch)
        # dl = None
        # if not dl_settings["simulated"]:
        #     from sensors.dl import DL
        #     dl = DL(dl_settings, batch)
        # rgb = None
        # if not settings["RGB"]["simulated"]:
        #     from sensors.rgb import RGB
        #     rgb = RGB(settings["RGB"])
        
        #alarm = Alarm(mqtt_client, alarm_settings, db, db_settings, data_lock, batch, stop_event)
        mqtt_userdata["db"] = db
        # mqtt_userdata["alarm"] = alarm
        # mqtt_userdata["rgb"] = rgb
        # mqtt_userdata["threads"] = threads
        
       # run_ds(mqtt_client, ds1_settings, batch, data_lock, threads, stop_event)
        run_ds(mqtt_client, ds2_settings, batch, data_lock, threads, stop_event)
        run_ds(mqtt_client, btn_settings, batch, data_lock, threads, stop_event, sd_settings)
       # run_dus(dus1_settings, threads, stop_event, batch, data_lock, dpir_dus_shared_dict)
        run_dus(dus2_settings, threads, stop_event, batch, data_lock, dpir_dus_shared_dict)
       # run_dpir(mqtt_client, dpir1_settings, threads, stop_event, batch, data_lock, dl, dl_settings, dus1_settings, dpir_dus_shared_dict, settings) ## AKO NIJE SIMULIRAN UREDJAJ PROSLEDITI Pravi DL objekat !!!!
        run_dpir(mqtt_client, dpir2_settings, threads, stop_event, batch, data_lock, None, dl_settings, dus2_settings, dpir_dus_shared_dict, settings)
        #run_dpir(dpir3_settings, threads, stop_event, batch, data_lock, None, dl_settings, None, None, settings, alarm)
       # run_db(db, db_settings, batch, data_lock, threads, stop_event)
        #run_dl(dl, dl_settings, batch, data_lock, threads, stop_event)
       # run_dms(mqtt_client, dms_settings, batch, data_lock, threads, stop_event)
        # run_dht(dht1_settings, threads, stop_event, data_lock, batch, dht_lct_shared_dict)
        # run_dht(dht2_settings, threads, stop_event, data_lock, batch, dht_lct_shared_dict)
        run_dht(dht3_settings, threads, stop_event, data_lock, batch, dht_lct_shared_dict)
        
        run_gyro(mqtt_client, gyro_settings, threads, stop_event, data_lock, batch)
        # run_lcd(lcd_settings, threads, stop_event, data_lock, batch, dht_lct_shared_dict)
        # run_ir(mqtt_client, ir_settings, threads, stop_event, rgb, rgb_settings)
        
        
        batch_thread =  threading.Thread(target=fill_batch, args=(mqtt_client, batch, data_lock, settings))
        batch_thread.start()
        threads.append(batch_thread)
        
        # run_dl1(dl1_settings, threads, stop_event)
        # run_dms(dms_settings, threads, stop_event)
        
        # cli_thread = threading.Thread(target = run_cli, args=(mqtt_client,data_lock, batch, settings, stop_event, db, dl, rgb, alarm, security_system, threads), daemon=True)
        # cli_thread.start()
        # threads.append(cli_thread)

        while not stop_event.is_set():
            time.sleep(0.5)


    except KeyboardInterrupt:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()
        for t in threads:
            stop_event.set()

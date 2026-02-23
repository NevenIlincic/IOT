import time
from simulators.dl import toggle_light
from simulators.dms import toggle_locked
from simulators.db import toggle_buzzer
from components.dms import dms_callback
from components.ir import ir_callback
from components.db import db_callback
from components.dl import dl_callback
from components.sd import sd_callback

import threading
from enum import Enum
from enums import State
from enums import Buzzing
from enums import DoorLightState

def run_cli(mqtt_client, data_lock, batch, settings, stop_event, db, dl, rgb, alarm, security_system, threads):
    dms_settings = settings['DMS']
    
    session = None
    smart_print_enabled = settings['PRINT']['activated']
    if smart_print_enabled:
        try:
            from prompt_toolkit.shortcuts import PromptSession
            session = PromptSession()
        except ImportError:
            smart_print_enabled = False
              
    while True:
        #command = input(">> ").strip().lower()
        try:
            if smart_print_enabled and session:
                    command = session.prompt(">> ").strip().lower()
            else:
                command = input(">> ").strip().lower()
            
            if command == "exit":
                stop_event.set()
            
            elif command == "dl":
                if settings["DL"]["simulated"]:
                    dl_callback(settings["DL"], data_lock, batch, stop_event, DoorLightState.ON.name)
                    time.sleep(10)
                    dl_callback(settings["DL"], data_lock, batch, stop_event, DoorLightState.OFF.name)
                    #toggle_light()
                else:
                    dl.toggle_light()
                    
            elif command == "db on":
                if settings["DB"]["simulated"]:
                    db_callback(settings["DB"], data_lock, batch, stop_event, Buzzing.BUZZING.name)
                   # toggle_buzzer()
                else:
                    db.toggle_buzz(True)
            elif command == "db off":
                if settings["DB"]["simulated"]:
                    db_callback(settings["DB"], data_lock, batch, stop_event, Buzzing.STOPPED.name)
                    #toggle_buzzer()
                else:
                    db.toggle_buzz(False)
            
            elif command == "alarm":
                if security_system.value == State.ON:
                    alarm.turn_on()

            elif command.startswith("ir") and settings["IR"]["simulated"]:
                arguments = command.split(" ")
                if len(arguments) >= 2:
                    if arguments[1] in ["0", "1", "2", "3", "4", "5", "6", "7"]:
                        ir_callback(mqtt_client, settings["IR"], rgb, settings["RGB"], stop_event, arguments[1])
            elif command.startswith("dms") and settings["DMS"]["simulated"]:
                arguments = command.split(" ")
                if len(arguments) >= 2:
                    try:
                        typed_password = arguments[1]
                        #toggle_locked(mqtt_client, dms_settings, typed_password)
                        dms_callback(mqtt_client, dms_settings, typed_password, alarm, security_system)
                    except:
                        print("Must be integer!")
                else:
                    print("Unknown command!") 
            elif command.startswith("start") and settings["4SD"]["simulated"]:
                arguments = command.split(" ")
                if len(arguments) == 2:
                    try:
                        seconds = int(arguments[1])
                        settings["4SD"]["seconds"] = seconds
                        
                        
                        sd_thread = threading.Thread(target = run_sd_counter, args=(settings, data_lock, batch, stop_event), daemon=True)
                        sd_thread.start()
                        threads.append(sd_thread)
                    except:
                        print("Must be integer")
                else:
                    print("Wrong command arguments!")
                    
            elif command == "btn":
                if settings["4SD"]["seconds"] > 0:
                    settings["4SD"]["seconds"] += 10
                elif settings["4SD"]["blinking"]:
                     settings["4SD"]["blinking"] = False
                     print("Stopped BLINKING")
                
            else:
                print("Unknown command!")
            
        
        except:
            print("Stopping app!")
            stop_event.set()
            break

def run_sd_counter(settings, data_lock, batch, stop_event):
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
        
    
import time
from simulators.dl import toggle_light
from simulators.dms import toggle_locked
from simulators.db import toggle_buzzer
from components.dms import dms_callback
from components.ir import ir_callback
import threading
from enum import Enum
from enums import State
# from sensors.rgb import RGB

def run_cli(mqtt_client, settings, stop_event, db, dl, alarm, security_system):
    dms_settings = settings['DMS']
    
    rgb = None
    if not settings["RGB"]["simulated"]:
        pass
        #rgb = RGB(settings["RGB"])
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
                    toggle_light()
                else:
                    dl.toggle_light()
                    
            elif command == "db on":
                if settings["DB"]["simulated"]:
                    toggle_buzzer()
                else:
                    db.toggle_buzz(True)
            elif command == "db off":
                if settings["DB"]["simulated"]:
                    toggle_buzzer()
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
            else:
                print("Unknown command!")
        except:
            print("Stopping app!")
            stop_event.set()
            break
        
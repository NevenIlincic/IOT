import time
from simulators.dl import toggle_light
from simulators.dms import toggle_locked
from simulators.db import toggle_buzzer
import threading


def run_cli(mqtt_client, settings, stop_event):
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
                toggle_light(mqtt_client, settings["DL"])
                    
            elif command == "db":
                toggle_buzzer(mqtt_client, settings["DB"])
                
            elif command.startswith("dms"):
                arguments = command.split(" ")
                if len(arguments) >= 2:
                    try:
                        typed_password = int(arguments[1])
                        toggle_locked(mqtt_client, dms_settings, typed_password)
                    
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
        
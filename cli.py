import time
from simulators.dl import toggle_light
from simulators.dms import toggle_locked
import threading

def buzz_worker():
    print("Buzzing...")
    time.sleep(2)
    print("Stopped buzzing!")

def run_cli(settings, stop_event):
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
                print(toggle_light())
                    
            elif command == "db":
                buzzer_thread = threading.Thread(target=buzz_worker, daemon=True)
                buzzer_thread.start()
                
            elif command.startswith("dms"):
                arguments = command.split(" ")
                if len(arguments) >= 2:
                    try:
                        typed_password = int(arguments[1])
                        dms_settings, message = toggle_locked(dms_settings, typed_password )
                        print(message)
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
        
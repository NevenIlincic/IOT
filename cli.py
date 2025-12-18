import time
from simulators.PI1.dl import toggle_light
from simulators.PI1.dms import toggle_locked
import threading

def buzz_worker():
    print("Buzzing...")
    time.sleep(2)
    print("Stopped buzzing!")

def run_cli(settings, stop_event):
    dms_settings = settings['DMS']
    while True:
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
            
        
import time
import random
from enum import Enum
import json


class Buzzing(Enum):
    BUZZING = 1
    STOPPED = 0


state = Buzzing.STOPPED

def toggle_buzzer():
    global state
    # string_to_return = ""
    if state == Buzzing.STOPPED:
        state = Buzzing.BUZZING
        #string_to_return = "Buzzing!"
    else:
        state = Buzzing.STOPPED
        #string_to_return = "Stopped buzzing!"
    
    

def generate_values():
    while True:
        yield state
      

def run_db_simulator(settings, data_lock, batch, stop_event, callback):
    for state in generate_values():
        callback(settings, data_lock, batch, stop_event, state.name)
        time.sleep(settings["delay"])  # Delay between readings (adjust as needed)
        if stop_event.is_set():
            break
              
# class Buzzing(Enum):
#     BUZZING = 1
#     STOPPED = 0

# def buzz_worker(mqtt_client, settings):
#     batch = []
#     data_to_send = {
#                 "name": settings["name"],
#                 "value": Buzzing.BUZZING.name,
#                 "simulated": True,
#                 "timestamp": time.time()
#             }
#     batch.append(data_to_send)
#     print("Buzzing...")
    
#     time.sleep(2)
#     data_to_send = {
#                 "name": settings["name"],
#                 "value": Buzzing.STOPPED.name,
#                 "simulated": True,
#                 "timestamp": time.time()
#             }
#     batch.append(data_to_send)
#     mqtt_client.publish(settings["topic"], json.dumps(batch))
#     print("Stopped buzzing!")
    
    
# def toggle_buzzer(mqtt_client, settings):
#     buzzer_thread = threading.Thread(target=buzz_worker, args=(mqtt_client, settings), daemon=True)
#     buzzer_thread.start()
    
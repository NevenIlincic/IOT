import time
import random
from enum import Enum
import threading
import json

class MotionDetected(Enum):
    DETECTED = 1
    NOT_DETECTED = 0

def generate_values(initial_state = MotionDetected.NOT_DETECTED):
    state = initial_state
    while True:
        x = random.randint(0,10)
        if x == 0:
            state = MotionDetected.DETECTED
        else:
            state = MotionDetected.NOT_DETECTED
        yield state

def run_dpir1_simulator(mqtt_client, settings, callback, stop_event):
        batch = []
        data_lock = threading.Lock()
        #Pokrecem batch nit                                                                  #prosledjuje se referenca na batch
        batch_thread = threading.Thread(target = run_batch_thread, args=(mqtt_client, settings, batch, data_lock, stop_event), daemon=True)
        batch_thread.start()
    
        for state in generate_values():
            time.sleep(settings['delay'])  # Delay between readings (adjust as needed)
            callback(state, "simulated")

            payload = {
                "name": settings["name"],
                "value": state.name,
                "simulated": True,
                "timestamp": time.time()
            }
            
            with data_lock:
                batch.append(payload)
                
            if stop_event.is_set():
                  break

def run_batch_thread(mqtt_client, settings, batch, data_lock, stop_event ):
    data_to_send = []
    while not stop_event.is_set():
        time.sleep(5)
        
        with data_lock:
            data_to_send = list(batch)
            batch.clear()
        
        if data_to_send:
            mqtt_client.publish(settings["topic"], json.dumps(data_to_send))
    
    with data_lock:
        if batch:
            mqtt_client.publish(settings["topic"], json.dumps(batch))
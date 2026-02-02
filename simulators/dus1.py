import time
import random
import json
import threading

def generate_values(initial_distance = 50.0):
      distance = initial_distance
      while True:
            distance += float(random.randint(-150, 150 )) / 10
            if distance < 0:
                  distance = 0
            yield round(distance, 1)

      

def run_dus1_simulator(mqtt_client, settings, callback, stop_event):
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
                  "value": state,
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
        time.sleep(10)
        
        with data_lock:
            data_to_send = list(batch)
            batch.clear()
        
        if data_to_send:
            mqtt_client.publish(settings["topic"], json.dumps(data_to_send))
    
    with data_lock:
        if batch:
            mqtt_client.publish(settings["topic"], json.dumps(batch))
import time
import json
import threading
from enum import Enum

class Buzzing(Enum):
    BUZZING = 1
    STOPPED = 0

def buzz_worker(mqtt_client, settings):
    batch = []
    data_to_send = {
                "name": settings["name"],
                "value": Buzzing.BUZZING.name,
                "simulated": True,
                "timestamp": time.time()
            }
    batch.append(data_to_send)
    print("Buzzing...")
    
    time.sleep(2)
    data_to_send = {
                "name": settings["name"],
                "value": Buzzing.STOPPED.name,
                "simulated": True,
                "timestamp": time.time()
            }
    batch.append(data_to_send)
    mqtt_client.publish(settings["topic"], json.dumps(batch))
    print("Stopped buzzing!")
    
    
def toggle_buzzer(mqtt_client, settings):
    buzzer_thread = threading.Thread(target=buzz_worker, args=(mqtt_client, settings), daemon=True)
    buzzer_thread.start()
    
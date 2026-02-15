from enum import Enum
import json
import time
from enums import AlarmState

class Alarm(object):
    def __init__(self, mqtt_client, settings):
        self.value = AlarmState.NOT_ACTIVE
        self.mqtt_client = mqtt_client
        self.settings = settings
    
    def turn_off(self):
        self.value = AlarmState.NOT_ACTIVE
        data_to_send = {
                    "name": self.settings["name"],
                    "value": self.value.name,
                    "timestamp": time.time()
                } 
        self.mqtt_client.publish(self.settings["topic"], json.dumps(data_to_send))
    
    def turn_on(self):
        self.value = AlarmState.ACTIVE
        data_to_send = {
                "name": self.settings["name"],
                "value": self.value.name,
                "timestamp": time.time()
            } 
        self.mqtt_client.publish(self.settings["topic"], json.dumps(data_to_send))
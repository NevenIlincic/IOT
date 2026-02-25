from enum import Enum
import json
import time
from enums import AlarmState, Buzzing
from components.db import db_callback


class Alarm(object):
    def __init__(self, mqtt_client, settings):
        self.value = AlarmState.NOT_ACTIVE
        self.mqtt_client = mqtt_client
        self.settings = settings

    def turn_off(self):
        print("ALARM ISKLJUCEN!")
        # if not self.db is None:
        #     self.db.toggle_buzz(False)
        # else:
        #     db_callback(self.db_settings, self.data_lock, self.batch, self.stop_event, Buzzing.STOPPED.name)
        self.value = AlarmState.NOT_ACTIVE
        data_to_send = {
                    "name": self.settings["name"],
                    "value": self.value.name,
                    "timestamp": time.time()
                } 
        self.mqtt_client.publish(self.settings["topic"], json.dumps(data_to_send))
    
        #Salje komandu da se buzzer iskljuci
        self.mqtt_client.publish("commands/buzzer", json.dumps({"action": "OFF"}))
    
    def turn_on(self):
        print("ALARM UKLJUCEN!")
        # if not self.db is None:
        #     self.db.toggle_buzz(True)
        # else:
        #     db_callback(self.db_settings, self.data_lock, self.batch, self.stop_event, Buzzing.BUZZING.name)
        self.value = AlarmState.ACTIVE
        data_to_send = {
                "name": self.settings["name"],
                "value": self.value.name,
                "timestamp": time.time()
            } 
        self.mqtt_client.publish(self.settings["topic"], json.dumps(data_to_send))
        self.mqtt_client.publish("commands/buzzer", json.dumps({"action": "ON"}))
import RPi.GPIO as GPIO
import time
from enum import Enum
from enums import DoorLightState

class DL(object):
    
    def __init__(self, dl_settings, batch):
        self.value = DoorLightState.OFF
        self.settings = dl_settings
        self.batch = batch
        self.PORT_BUZZER = self.settings["pin"]
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PORT_BUZZER,GPIO.OUT)
        
    def toggle_light(self):
        GPIO.output(self.PORT_BUZZER,GPIO.HIGH) #Upaljen
        self.value = DoorLightState.ON
        time.sleep(10)
        self.value = DoorLightState.OFF
        GPIO.output(self.PORT_BUZZER,GPIO.LOW) #Ugasen
             
def run_dl_loop(dl, settings, data_lock, batch, stop_event, callback):
    while True:
        callback(settings, data_lock, batch, stop_event, dl.value.name)
        time.sleep(settings["delay"])
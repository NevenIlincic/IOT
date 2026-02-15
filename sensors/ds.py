import RPi.GPIO as GPIO
from enum import Enum
from components.ds1 import run_ds
import time
from enums import DoorState

class DS(object):

    def __init__(self, ds_settings, batch):
        self.value = DoorState.CLOSED
        self.settings = ds_settings
        self.batch = batch
        self.PORT_BUTTON = ds_settings["pin"] #17
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PORT_BUTTON, GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(self.PORT_BUTTON, GPIO.BOTH, callback = self.button_pressed, bouncetime = 100)
        #GPIO.add_event_detect(self.PORT_BUTTON, GPIO.RISING, callback = self.button_released, bouncetime = 100)
    
    def button_pressed(self, event):
        if GPIO.input(self.PORT_BUTTON) == GPIO.LOW:
            self.value = DoorState.OPEN      # pritisnuto
        else:
            self.value = DoorState.CLOSED 
       # self.value = DoorState.OPEN
    # def button_released(self, event):
    #     self.value = DoorState.CLOSED

def run_ds_loop(ds, settings, data_lock, batch, stop_event, callback ):
    while True:
        callback(settings, data_lock, batch, stop_event, ds.value.name)
        time.sleep(settings["delay"])
    
    

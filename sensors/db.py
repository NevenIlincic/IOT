import RPi.GPIO as GPIO
import time
from enum import Enum


class Buzzing(Enum):
    BUZZING = 1
    STOPPED = 0

class DB(object):
    
    def __init__(self, db_settings, batch):
        self.value = Buzzing.STOPPED
        self.settings = db_settings
        self.batch = batch
        self.PORT_BUZZER = self.settings["pin"]
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PORT_BUZZER, GPIO.OUT)
        
    def toggle_buzz(self):
        if self.value == Buzzing.BUZZING:
            self.value = Buzzing.STOPPED
            GPIO.output(self.PORT_BUZZER, False)
        else:
            self.value = Buzzing.BUZZING
            GPIO.output(self.PORT_BUZZER, True)
            # period = 1.0 / pitch
            # delay = period / 2
            # cycles = int(duration * pitch)
            # for i in range(cycles):
            # GPIO.output(buzzer_pin, True)
            # time.sleep(delay)
            # GPIO.output(buzzer_pin, False)
            # time.sleep(delay)
        
          
def run_db_loop(db, settings, data_lock, batch, stop_event, callback):
    while True:
        callback(settings, data_lock, batch, stop_event, db.value.name)
        time.sleep(settings["delay"])
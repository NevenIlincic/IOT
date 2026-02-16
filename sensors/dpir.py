import RPi.GPIO as GPIO
from enums import MotionDetected
import time

class DPIR(object):
    def __init__(self, dpir_settings):
        self.value = MotionDetected.NOT_DETECTED
        self.settings = dpir_settings
        self.PIR_PIN = dpir_settings["pin"]
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIR_PIN, GPIO.IN)
        
        GPIO.add_event_detect(self.PIR_PIN, GPIO.RISING, callback=self.motion_detected)
        GPIO.add_event_detect(self.PIR_PIN, GPIO.FALLING, callback=self.no_motion)
        
    def motion_detected(self, channel):
        self.value = MotionDetected.DETECTED
        
    def no_motion(self, channel):
        self.value = MotionDetected.NOT_DETECTED

def run_dpir_loop(dpir: DPIR, dpir_settings, data_lock, batch, stop_event, callback):
    while True:
        callback(dpir_settings, data_lock, batch, stop_event, dpir.value)
        time.sleep(dpir_settings["delay"])
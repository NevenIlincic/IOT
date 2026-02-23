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
        
        GPIO.add_event_detect(self.PIR_PIN, GPIO.BOTH, callback=self.edge_callback)
        
    # def motion_detected(self, channel):
    #     self.value = MotionDetected.DETECTED
        
    # def no_motion(self, channel):
    #     self.value = MotionDetected.NOT_DETECTED
    
    def edge_callback(self, channel):
        if GPIO.input(channel):
            self.value = MotionDetected.DETECTED
        else:
            self.value = MotionDetected.NOT_DETECTED

def run_dpir_loop(dpir: DPIR, dpir_settings, data_lock, batch, stop_event, callback, dl, dl_settings, dus_settings, dpir_dus_shared_dict, all_settings, alarm):
    while True:
        callback(dpir_settings, dl, dl_settings, data_lock, batch, stop_event, dpir.value, dus_settings, dpir_dus_shared_dict, all_settings, alarm)
        time.sleep(dpir_settings["delay"])
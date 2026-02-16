import RPi.GPIO as GPIO
import time


class DUS(object):
    def __init__(self, dus_settings):
        self.value = 0
        self.settings = dus_settings
        GPIO.setmode(GPIO.BCM)

        self.TRIG_PIN = self.settings["TRIG_PIN"]  #23
        self.ECHO_PIN = self.settings["ECHO_PIN"] #24

        GPIO.setup(self.TRIG_PIN, GPIO.OUT)
        GPIO.setup(self.ECHO_PIN, GPIO.IN)

    def get_distance(self):
        GPIO.output(self.TRIG_PIN, False)
        time.sleep(0.2)
        GPIO.output(self.TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(self.TRIG_PIN, False)
        pulse_start_time = time.time()
        pulse_end_time = time.time()

        max_iter = 100

        iter = 0
        while GPIO.input(self.ECHO_PIN) == 0:
            if iter > max_iter:
                return None
            pulse_start_time = time.time()
            iter += 1

        iter = 0
        while GPIO.input(self.ECHO_PIN) == 1:
            if iter > max_iter:
                return None
            pulse_end_time = time.time()
            iter += 1

        pulse_duration = pulse_end_time - pulse_start_time
        distance = (pulse_duration * 34300)/2
        return distance

def run_dus_loop(dus: DUS, dus_settings, data_lock, batch, stop_event, callback):
    while True:
        callback(dus_settings, data_lock, batch, stop_event, dus.value)
        time.sleep(dus_settings["delay"])
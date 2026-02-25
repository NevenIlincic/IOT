import RPi.GPIO as GPIO
import time

class DMS(object):
    def __init__(self, dms_settings, batch, data_lock, mqtt_client):
        self.value = ""
        self.settings = dms_settings
        self.batch = batch
        self.data_lock = data_lock
        self.mqtt_client = mqtt_client
        
        self.R1 = dms_settings["R1"]
        self.R2 = dms_settings["R2"]
        self.R3 = dms_settings["R3"]
        self.R4 = dms_settings["R4"]

        self.C1 = dms_settings["C1"]
        self.C2 = dms_settings["C2"]
        self.C3 = dms_settings["C3"]
        self.C4 = dms_settings["C4"]

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.R1, GPIO.OUT)
        GPIO.setup(self.R2, GPIO.OUT)
        GPIO.setup(self.R3, GPIO.OUT)
        GPIO.setup(self.R4, GPIO.OUT)

        GPIO.setup(self.C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    def readLine(self, line, characters, stop_event, callback):
        GPIO.output(line, GPIO.HIGH)
        if(GPIO.input(self.C1) == 1):
            if line == self.R4:
                self.value = ""
            else:
                self.value += characters[0]
                print("INPUT: " + self.value)
        if(GPIO.input(self.C2) == 1):
            self.value += characters[1]
            print("INPUT: " + self.value)
        if(GPIO.input(self.C3) == 1):
            if line == self.R4:
                if not len(self.value) == 0:
                    callback(self.mqtt_client, self.settings, self.value, self.alarm, self.security_system)
                    self.value = ""
                    print("INPUT SENT")
            else:
                self.value += characters[2]
                print("INPUT: " + self.value)
        if(GPIO.input(self.C4) == 1):
            self.value += characters[3]
            print("INPUT: " + self.value)
        
        GPIO.output(line, GPIO.LOW)


def run_dms_loop(dms, stop_event, callback):
    try:
        while True:
            # call the readLine function for each row of the keypad
            dms.readLine(dms.R1, ["1","2","3","A"], stop_event, callback)
            dms.readLine(dms.R2, ["4","5","6","B"], stop_event, callback)
            dms.readLine(dms.R3, ["7","8","9","C"], stop_event, callback)
            dms.readLine(dms.R4, ["*","0","#","D"], stop_event, callback)
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nApplication stopped!")
        



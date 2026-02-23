import RPi.GPIO as GPIO
from time import sleep
from enums import RGBColor

class RGB(object):
    def __init__(self, rgb_settings):
        self.value = RGBColor.OFF
        self.settings = rgb_settings

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        self.RED_PIN = self.settings["RED_PIN"]   #12
        self.GREEN_PIN = self.settings["GREEN_PIN"]  #13
        self.BLUE_PIN = self.settings["BLUE_PIN"] #19

        #set pins as outputs
        GPIO.setup(self.RED_PIN, GPIO.OUT)
        GPIO.setup(self.GREEN_PIN, GPIO.OUT)
        GPIO.setup(self.BLUE_PIN, GPIO.OUT)
    
    def change_color(self, value):
        if value == "0":
            self.turnOff()
            self.value = RGBColor.OFF
        elif value == "1":
            self.white()
            self.value = RGBColor.WHITE
        elif value == "2":
            self.red()
            self.value = RGBColor.RED
        elif value == "3":
            self.green()
            self.value = RGBColor.GREEN
        elif value == "4":
            self.blue()
            self.value = RGBColor.BLUE
        elif value == "5":
            self.yellow()
            self.value = RGBColor.YELLOW
        elif value == "6":
            self.purple()
            self.value = RGBColor.PURPLE
        elif value == "7":
            self.lightBlue()
            self.value = RGBColor.LIGHT_BLUE

    def turnOff(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)
        
    def white(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
        
    def red(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)

    def green(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)
        
    def blue(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
        
    def yellow(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.LOW)
        
    def purple(self):
        GPIO.output(self.RED_PIN, GPIO.HIGH)
        GPIO.output(self.GREEN_PIN, GPIO.LOW)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)
        
    def lightBlue(self):
        GPIO.output(self.RED_PIN, GPIO.LOW)
        GPIO.output(self.GREEN_PIN, GPIO.HIGH)
        GPIO.output(self.BLUE_PIN, GPIO.HIGH)

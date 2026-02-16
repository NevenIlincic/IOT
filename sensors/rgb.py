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
        match value:
            case "0":
                self.turnOff()
                self.value = RGBColor.OFF
            case "1":
                self.white()
                self.value = RGBColor.WHITE
            case "2":
                self.red()
                self.value = RGBColor.RED
            case "3":
                self.green()
                self.value = RGBColor.GREEN
            case "4":
                self.blue()
                self.value = RGBColor.BLUE
            case "5":
                self.yellow()
                self.value = RGBColor.YELLOW
            case "6":
                self.purple()
                self.value = RGBColor.PURPLE
            case "7":
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

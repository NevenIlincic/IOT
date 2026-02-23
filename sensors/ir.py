import RPi.GPIO as GPIO
from datetime import datetime
import time

class IR(object):
    def __init__(self, ir_settings):
        self.settings = ir_settings
        self.pin = ir_settings["pin"] #17
        self.Buttons = [0x300ff22dd, 0x300ffc23d, 0x300ff629d, 0x300ffa857, 0x300ff9867, 0x300ffb04f, 0x300ff6897, 0x300ff02fd, 0x300ff30cf, 0x300ff18e7, 0x300ff7a85, 0x300ff10ef, 0x300ff38c7, 0x300ff5aa5, 0x300ff42bd, 0x300ff4ab5, 0x300ff52ad]  # HEX code list
        self.ButtonsNames = ["LEFT",   "RIGHT",      "UP",       "DOWN",       "2",          "3",          "1",        "OK",        "4",         "5",         "6",         "7",         "8",          "9",        "*",         "0",        "#"]  # String list in same order as HEX list

        # Sets up GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.IN)




    def getBinary(self):
        num1s = 0  # Number of consecutive 1s read
        binary = 1  # The binary value
        command = []  # The list to store pulse times in
        previousValue = 0  # The last value
        value = GPIO.input(self.pin)  # The current value

        while value:
            time.sleep(0.0001) # This sleep decreases CPU utilization immensely
            value = GPIO.input(self.pin)
            
        # Records start time
        startTime = datetime.now()
        
        while True:
            # If change detected in value
            if previousValue != value:
                now = datetime.now()
                pulseTime = now - startTime #Calculate the time of pulse
                startTime = now #Reset start time
                command.append((previousValue, pulseTime.microseconds)) #Store recorded data
                
            # Updates consecutive 1s variable
            if value:
                num1s += 1
            else:
                num1s = 0
            
            # Breaks program when the amount of 1s surpasses 10000
            if num1s > 10000:
                break
                
            # Re-reads pin
            previousValue = value
            value = GPIO.input(self.pin)
            
        # Converts times to binary
        for (typ, tme) in command:
            if typ == 1: #If looking at rest period
                if tme > 1000: #If pulse greater than 1000us
                    binary = binary *10 +1 #Must be 1
                else:
                    binary *= 10 #Must be 0
                
        if len(str(binary)) > 34: #Sometimes, there is some stray characters
            binary = int(str(binary)[:34])
            
        return binary
        
    # Convert value to hex
    def convertHex(self, binaryValue):
        tmpB2 = int(str(binaryValue),2) #Temporarely propper base 2
        return hex(tmpB2)

# def run_ir_loop(mqtt_client, ir: IR, ir_settings, stop_event, callback): 
#     while True:
#         inData = ir.convertHex(ir.getBinary()) #Runs subs to get incoming hex value
#         for button in range(len(ir.Buttons)):#Runs through every value in list
#             if hex(ir.Buttons[button]) == inData: #Checks this against incoming
#                 if (hex(ir.Buttons[button]) in ["0", "1", "2", "3", "4", "5", "6", "7"]):
#                     callback(mqtt_client, ir_settings, stop_event, hex(ir.Buttons[button]))

def run_ir_loop(mqtt_client, ir: IR, ir_settings, stop_event, callback, rgb, rgb_settings): 
    while not stop_event.is_set():
        # 1. Uzmi binarnu vrednost i konvertuj u HEX
        binary_val = ir.getBinary()
        inData = ir.convertHex(binary_val) 
        
        # Debug: ispiši šta je senzor zapravo očitao
        if inData != "0x1": # 0x1 je često default kad nema signala
             print(f"Očitani HEX: {inData}")

        # 2. Prođi kroz definisane kodove u self.Buttons
        for i in range(len(ir.Buttons)):
            if hex(ir.Buttons[i]) == inData:
                button_name = ir.ButtonsNames[i]
                print(f"Pritisnuto dugme: {button_name}")

                # 3. Ako je pritisnuto dugme koje je broj (0-7), pošalji taj broj
                if button_name in ["0", "1", "2", "3", "4", "5", "6", "7"]:
                    # Ovde šalješ "0", "1" itd. kao string, što tvoj callback očekuje
                    callback(mqtt_client, ir_settings, rgb, rgb_settings, stop_event, button_name)
#!/usr/bin/env python3

from sensors.lcd.PCF8574 import PCF8574_GPIO
from sensors.lcd.Adafruit_LCD1602 import Adafruit_CharLCD

from time import sleep, strftime
from datetime import datetime
 
 
def get_cpu_temp():     # get CPU temperature and store it into file "/sys/class/thermal/thermal_zone0/temp"
    tmp = open('/sys/class/thermal/thermal_zone0/temp')
    cpu = tmp.read()
    tmp.close()
    return '{:.2f}'.format( float(cpu)/1000 ) + ' C'
 
def get_time_now():     # get system time
    return datetime.now().strftime('    %H:%M:%S')

        
def run_lcd_loop(lcd_settings, callback, data_lock, batch, stop_event, lcd_values_dict):
    global temp_string, humidity_string
    mcp.output(3,1)     # turn on LCD backlight
    lcd.begin(16,2)     # set number of LCD lines and columns
    i = 0
    while(True):       
        #lcd.clear()
        lcd.setCursor(0,0)  # set cursor position
        
        temp_string = lcd_values_dict["temp_string"]
        humidity_string = lcd_values_dict["humidity_string"]
        
        lcd.message(temp_string)
        lcd.message(humidity_string)
        callback(lcd_settings, data_lock, batch, temp_string, humidity_string, stop_event)
        sleep(lcd_settings["delay"])
        i = (i+1) % 3
        
def destroy():
    lcd.clear()
    
PCF8574_address = 0x27  # I2C address of the PCF8574 chip.
PCF8574A_address = 0x3F  # I2C address of the PCF8574A chip.
# Create PCF8574 GPIO adapter.
try:
	mcp = PCF8574_GPIO(PCF8574_address)
except:
	try:
		mcp = PCF8574_GPIO(PCF8574A_address)
	except:
		print ('I2C Address Error !')
		exit(1)
# Create LCD, passing in MCP GPIO adapter.
lcd = Adafruit_CharLCD(pin_rs=0, pin_e=2, pins_db=[4,5,6,7], GPIO=mcp)

if __name__ == '__main__':
    print ('Program is starting ... ')
    try:
        loop()
    except KeyboardInterrupt:
        destroy()


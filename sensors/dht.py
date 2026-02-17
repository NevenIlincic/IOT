
import RPi.GPIO as GPIO
import time

class DHT(object):
	DHTLIB_OK = 0
	DHTLIB_ERROR_CHECKSUM = -1
	DHTLIB_ERROR_TIMEOUT = -2
	DHTLIB_INVALID_VALUE = -999
	
	DHTLIB_DHT11_WAKEUP = 0.020#0.018		#18ms
	DHTLIB_TIMEOUT = 0.0001			#100us
	
	humidity = 0
	temperature = 0
	
	def __init__(self, dht_settings):
		self.settings = dht_settings
		self.pin = self.settings["pin"]
		self.bits = [0,0,0,0,0]
		self.humidity = 20
		self.temperature = 20
  
	#Read DHT sensor, store the original data in bits[]	
	def readSensor(self,wakeupDelay):
		mask = 0x80
		idx = 0
		self.bits = [0,0,0,0,0]
		GPIO.setup(self.pin,GPIO.OUT)
		GPIO.output(self.pin,GPIO.LOW)
		time.sleep(wakeupDelay)
		GPIO.output(self.pin,GPIO.HIGH)
		#time.sleep(40*0.000001)
		GPIO.setup(self.pin,GPIO.IN)
		
		loopCnt = self.DHTLIB_TIMEOUT
		t = time.time()
		while(GPIO.input(self.pin) == GPIO.LOW):
			if((time.time() - t) > loopCnt):
				return self.DHTLIB_ERROR_TIMEOUT
		t = time.time()
		while(GPIO.input(self.pin) == GPIO.HIGH):
			if((time.time() - t) > loopCnt):
				return self.DHTLIB_ERROR_TIMEOUT
		for i in range(0,40,1):
			t = time.time()
			while(GPIO.input(self.pin) == GPIO.LOW):
				if((time.time() - t) > loopCnt):
					return self.DHTLIB_ERROR_TIMEOUT
			t = time.time()
			while(GPIO.input(self.pin) == GPIO.HIGH):
				if((time.time() - t) > loopCnt):
					return self.DHTLIB_ERROR_TIMEOUT		
			if((time.time() - t) > 0.00005):	
				self.bits[idx] |= mask
			mask >>= 1
			if(mask == 0):
				mask = 0x80
				idx += 1	
		GPIO.setup(self.pin,GPIO.OUT)
		GPIO.output(self.pin,GPIO.HIGH)
		return self.DHTLIB_OK

	def readDHT11(self):
		rv = self.readSensor(self.pin,self.DHTLIB_DHT11_WAKEUP)
		if (rv is not self.DHTLIB_OK):
			self.humidity = self.DHTLIB_INVALID_VALUE
			self.temperature = self.DHTLIB_INVALID_VALUE
			return rv
		self.humidity = self.bits[0]
		self.temperature = self.bits[2] + self.bits[3]*0.1
		sumChk = ((self.bits[0] + self.bits[1] + self.bits[2] + self.bits[3]) & 0xFF)
		if(self.bits[4] is not sumChk):
			return self.DHTLIB_ERROR_CHECKSUM
		return self.DHTLIB_OK

def parseCheckCode(code):
	if code == 0:
		return "DHTLIB_OK"
	elif code == -1:
		return "DHTLIB_ERROR_CHECKSUM"
	elif code == -2:
		return "DHTLIB_ERROR_TIMEOUT"
	elif code == -999:
		return "DHTLIB_INVALID_VALUE"


def run_dht_loop(dht: DHT, data_lock, batch, callback, stop_event):
		while True:
			humidity, temperature = dht.humidity, dht.temperature
			settings = dht.settings
			callback(settings, data_lock, batch, temperature, humidity, stop_event)
			if stop_event.is_set():
					break
			time.sleep(settings["delay"])

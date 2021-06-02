import RPi.GPIO as GPIO
import dht11
import smbus
import time
import datetime

# initialize GPIO
relay_pin1 = 21
address = 0x48
A0 = 0x40



GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pin1, GPIO.OUT)

# read data using pin 14
instance = dht11.DHT11(pin=17)

bus = smbus.SMBus(1)

def relay_on(pin):
    GPIO.output(pin, GPIO.LOW)

def relay_off(pin):
    GPIO.output(pin, GPIO.HIGH)

def is_relay_on(pin):
    return not GPIO.input(pin)


def humidityOutOfRange(result):
    if (result.humidity < 40 or result.humidity >60):
        print("Shitty Humidity, alarming")
        return True
    else:
        return False

def tempOutOfRange(result):
    if (result.temperature < 20 or result.temperature > 28):
        print("Shitty temp,alarming")
        return True
    else:
        return False
def validateParams(result):
        if (humidityOutOfRange(result) or tempOutOfRange(result)):
            if is_relay_on(relay_pin1) != True:
                    print("Turning Relay On")
                    relay_on(relay_pin1)
                #print("Shitty humidity, alarm")
        elif is_relay_on(relay_pin1) == True:
                relay_off(relay_pin1)
                print("Switching relay off since Ideal Param range")





try:
	while True:
            #bus.write_byte(address, A0)

            value = bus.read_byte(address)
            time.sleep(0.1)
            print("Digital value coming in as: %-3.1f " % value)
	    result = instance.read()
	    if result.is_valid():
	        print("Last valid input: " + str(datetime.datetime.now()))

	        print("Temperature: %-3.1f C" % result.temperature)
		print("Temperature: %-3.1f F" % (result.temperature*9/5 + 32))
	        print("Humidity: %-3.1f %%" % result.humidity)
		validateParams(result)
		print("Raw Result: " + str(result))
	    time.sleep(10)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()

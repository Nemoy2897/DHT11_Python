import RPi.GPIO as GPIO
import smbus
import time
import datetime


address = 0x48

A0 = 0x40


GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)



bus = smbus.SMBus(1)

def read(control):
    bus.write_byte_data(address, control, 0)
    return bus.read_byte(address)

try:
    while True:
        value = []
        temp = 0
        for i in range(10):
            temp = read(A0)
            value.append(temp)
            print("temp/1024 is: " + str(temp/1024))
            print("temp is: " + str(temp))
        value.sort()
        sum1 = 0
        for i in range(1,7):
            sum1 = sum1 + value[i]
            print("sum is now: "+ str(sum1))
        Voltage = float(sum1)/(6)
        pHValue = 3.5*Voltage

        print("Voltage is coming as:  " + str(Voltage))
        #print("EC Value is coming as: " + str(pHValue))
        time.sleep(5)

except KeyboardInterrupt:
    print("wassup")
    GPIO.cleanup

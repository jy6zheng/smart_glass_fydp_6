import time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

HIGH = True
LOW = False

SCLK = 21
MISO = 20
CE = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(SCLK, GPIO.OUT)
GPIO.setup(MISO, GPIO.IN)
GPIO.setup(CE, GPIO.OUT)

class Potentiometer():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SCLK, GPIO.OUT)
        GPIO.setup(MISO, GPIO.IN)
        GPIO.setup(CE, GPIO.OUT)
        
    def readData(self, SCLK, MISO, CE):
        # max value is 252 and min value is 0
        GPIO.output(CE, LOW)
        GPIO.output(SCLK, LOW)
        
        adcvalue = 0
        for i in range(10):
            GPIO.output(SCLK, HIGH)
            GPIO.output(SCLK, LOW)
            adcvalue <<= 1
            if(GPIO.input(MISO)):
                adcvalue |= 0x1
        GPIO.output(CE, HIGH)
        time.sleep(0.5)
        
        return adcvalue

# while True:
#     print(readData(SCLK, MISO, CE))
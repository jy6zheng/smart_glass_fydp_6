import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

# set up the GPIO pins
A0 = 5
A1 = 6
A2 = 13
EN = 26

class Mux():
    # A2 A1 A0
    # 0  0  0  0V
    # 0  0  1  7V
    # 0  1  0  14V
    # 0  1  1  21V
    # 1  0  0  28V
    # 1  0  1  35V
    # 1  1  0  42V
    # 1  1  1  49V
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(A0, GPIO.OUT)
        GPIO.setup(A1, GPIO.OUT)
        GPIO.setup(A2, GPIO.OUT)
        GPIO.setup(EN, GPIO.OUT)
    
    def opaque(self):
        GPIO.output(EN, 0)
        GPIO.output(A2, 0)
        GPIO.output(A1, 0)
        GPIO.output(A0, 0)
        GPIO.output(EN, 1)
        

    def level_1(self):
        # transparency levels go from least transparent level 0 to level 8 most
        GPIO.output(EN, 0)
        GPIO.output(A2, 0)
        GPIO.output(A1, 0)
        GPIO.output(A0, 1)
        GPIO.output(EN, 1)
        
    def level_2(self):
        # 14 V
        GPIO.output(EN, 0)
        GPIO.output(A2, 0)
        GPIO.output(A1, 1)
        GPIO.output(A0, 0)
        GPIO.output(EN, 1)
    
    def level_3(self):
        # 21 V
        GPIO.output(EN, 0)
        GPIO.output(A2, 0)
        GPIO.output(A1, 1)
        GPIO.output(A0, 1)
        GPIO.output(EN, 1)
    
    def level_4(self):
        # 28 V
        GPIO.output(EN, 0)
        GPIO.output(A2, 1)
        GPIO.output(A1, 0)
        GPIO.output(A0, 0)
        GPIO.output(EN, 1)
    
    def level_5(self):
        # 35 V
        GPIO.output(EN, 0)
        GPIO.output(A2, 1)
        GPIO.output(A1, 0)
        GPIO.output(A0, 1)
        GPIO.output(EN, 1)
    
    def level_6(self):
        # 42 V
        GPIO.output(EN, 0)
        GPIO.output(A2, 1)
        GPIO.output(A1, 1)
        GPIO.output(A0, 0)
        GPIO.output(EN, 1)
    
    def transparent(self):
        # 49 V
        GPIO.output(EN, 0)
        GPIO.output(A2, 1)
        GPIO.output(A1, 1)
        GPIO.output(A0, 1)
        GPIO.output(EN, 1)
    
     


import logging
import threading
from threading import Thread
import time
from transparency import *
from light_sensor import *
from time import *

# right now can either be 1 (fully transparent) or 0 (completely opaque)
CURRENT_STATE = 0
def transparency():
    transparency = Mux()
    while True:
        if CURRENT_STATE == 1:
            transparency.transparent()
        else:
            transparency.opaque()

transparency = Thread(target=transparency)
transparency.start()

def light_sensor_mode(difference):
        # NOTE: going to add feature that considers magnitude
        # positive indicates outside is brighter
        if difference > 1:
            print("increase natural light")
            return 1
        else:
            print("increase privacy")
            return 0

while True:
    light_sensor = LightSensor()
    console_input = input("operation mode number: ") 
    if console_input == "1":
        print("regular mode")
        if CURRENT_STATE == 0:
            print("transparent")
            CURRENT_STATE = 1
        else:
            print("opaque")
            CURRENT_STATE = 0
    elif console_input == "2":
        print("light sensing mode")
        try:
            while(True):
                difference = light_sensor.read_light()
                CURRENT_STATE = light_sensor_mode(difference)
        except KeyboardInterrupt:
            continue
    elif console_input == "3":
        print("timer mode")
        setting = input("transparent (1) or opaque (0): ")
        setting_time = input("input time as s:m:h ")
        setting_time = setting_time.split(":")
        time_sec = 0
        for i in range(len(setting_time)):
            time_sec += int(setting_time[i]) * 60 ** i
        print("changing transparency for {} seconds".format(time_sec))
        CURRENT_STATE = int(setting)
        sleep(time_sec)
        print("timer finished")
        if CURRENT_STATE > 0:
            CURRENT_STATE = 0
            print("turning opaque")
        else:
            CURRENT_STATE = 1
            print("turning transparent")
        
        
        
                
                
        
    
            
    
    


    
        

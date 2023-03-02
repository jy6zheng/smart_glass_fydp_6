import logging
import threading
from threading import Thread
import time
from transparency import *
from light_sensor import *

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

while True:
    console_input = input("operation mode number: ") 
    if console_input == "1":
        print("regular mode")
        if CURRENT_STATE == 0:
            print("transparent")
            CURRENT_STATE = 1
        else:
            print("opaque")
            CURRENT_STATE = 0
    


    
        

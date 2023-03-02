import logging
import threading
from threading import Thread
import time
import I2C_LCD_driver
from transparency import *
from light_sensor import *
from time import *
from potentiometer import *

# right now can either be 1 (fully transparent) or 0 (completely opaque)
CURRENT_STATE = 0
GRAD_READING = 0

def transparency():
    transparency = Mux()
    while True:
        if CURRENT_STATE == 1:
            transparency.transparent()
        elif CURRENT_STATE == 2:
            transparency.level_1()
        elif CURRENT_STATE == 3:
            transparency.level_2()
        elif CURRENT_STATE == 4:
            transparency.level_3()
        elif CURRENT_STATE == 5:
            transparency.level_4()
        elif CURRENT_STATE == 6:
            transparency.level_5()
        elif CURRENT_STATE == 7:
            transparency.level_6()
        else:
            transparency.opaque()

def gradient():
    global GRAD_READING
    SCLK = 21
    MISO = 20
    CE = 16
    potentiometer = Potentiometer()
    while True:
        GRAD_READING = potentiometer.readData(SCLK, MISO, CE) // 32 # since we have 8 settings

transparency = Thread(target=transparency)
gradient = Thread(target=gradient)
transparency.start()
gradient.start()
            
def light_sensor_mode(difference):
        # NOTE: going to add feature that considers magnitude
        # positive indicates outside is brighter
        if difference > 1:
            print("increase natural light")
            return 1
        else:
            print("increase privacy")
            return 0
lcd = I2C_LCD_driver.lcd()
lcd.lcd_display_string("starting up...", 1)
sleep(1)
try:
    while True:
        print(CURRENT_STATE)
        lcd.lcd_clear()
        light_sensor = LightSensor()
        lcd.lcd_display_string("input mode number:", 1)
        console_input = input("operation mode number: ")
        lcd.lcd_clear()
        if console_input == "1":
            lcd.lcd_display_string("regular mode", 1)
            print("regular mode")
            if CURRENT_STATE == 0:
                lcd.lcd_display_string("turning transparent", 2)
                print("transparent")
                CURRENT_STATE = 1
            else:
                lcd.lcd_display_string("turning opaque", 2)
                print("opaque")
                CURRENT_STATE = 0
            sleep(2)
        elif console_input == "2":
            print("privacy mode")
            try:
                previous_state = None
                while(True):
                    difference = light_sensor.read_light()
                    CURRENT_STATE = light_sensor_mode(difference)
                    if previous_state != CURRENT_STATE:
                        lcd.lcd_clear()
                        lcd.lcd_display_string("privacy mode", 1)
                        if CURRENT_STATE == 1:
                            lcd.lcd_display_string("increasing light", 2)
                        else:
                            lcd.lcd_display_string("increasing privacy", 2)
                    previous_state = CURRENT_STATE
            except KeyboardInterrupt:
                lcd.lcd_clear()
                continue
        elif console_input == "3":
            print("timer mode")
            lcd.lcd_display_string("timer mode", 1)
            lcd.lcd_display_string("clear(1) / opaque(0)", 2)
            setting = input("transparent (1) or opaque (0): ")
            lcd.lcd_display_string("input time ss:mm:hh", 3)
            setting_time = input("input time as s:m:h ")
            setting_time = setting_time.split(":")
            time_sec = 0
            for i in range(len(setting_time)):
                time_sec += int(setting_time[i]) * 60 ** i
            if setting == "1":
                lcd.lcd_display_string("clear for {}s".format(time_sec), 4)
            else:
                lcd.lcd_display_string("opaque for {}s".format(time_sec), 4)
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
            lcd.lcd_clear()
            lcd.lcd_display_string("finished timer")
            sleep(2)
        elif console_input == "4":
            print("gradient mode")
            lcd.lcd_display_string("gradient mode", 1)
            lcd.lcd_display_string("adjust from 1-8", 2)
            lcd.lcd_display_string("Ctrl-C to enter", 3)
            previous_gradient = GRAD_READING
            lcd.lcd_display_string("level {}".format(GRAD_READING), 4)
            try:
                while True:
                    if previous_gradient != GRAD_READING:
                        lcd.lcd_display_string("level {}".format(GRAD_READING), 4)
                        previous_gradient = GRAD_READING
            except KeyboardInterrupt:
                lcd.lcd_clear()
                lcd.lcd_display_string("gradient mode", 1)
                lcd.lcd_display_string("Gradient level {}%".format(GRAD_READING / 8 * 100), 2)
                CURRENT_STATE = GRAD_READING
                sleep(2)
                continue
        else:
            print("invalid mode")
            lcd.lcd_display_string("invalid mode entered", 1)
except KeyboardInterrupt:
    lcd.lcd_clear()
    lcd.lcd_display_string("shutting down", 1)
    sleep(3)
    lcd.lcd_clear()
    CURRENT_STATE = 0
    raise SystemExit
        
        
                
                
        
    
            
    
    


    
        

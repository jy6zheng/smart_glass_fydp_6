import time
from transparency import *
from light_sensor import *
import I2C_LCD_driver
from time import *


class Window():
    def __init__(self):
        self.current_state = 0
        self.transparency = Mux()
        self.light_sensor = LightSensor()
        self.lcd = I2C_LCD_driver.lcd()
    
    def regular_mode(self):
        if self.current_state == 0:
            self.transparency.transparent()
            self.current_state = 1
            self.lcd.lcd_display_string("turning transparent", 2)
            print("turning transparent")
        else:
            self.transparency.opaque()
            self.current_state = 0
            self.lcd.lcd_display_string("turning opaque", 2)
            print("turning opaque")
    
    def light_sensor_mode(self):
        difference = self.light_sensor.read_light()
        # NOTE: going to add feature that considers magnitude
        # positive indicates outside is righter
        if difference > 1:
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string("increase natural light", 2)
            print("increase natural light")
            self.transparency.transparent()
        else:
            self.lcd.lcd_clear()
            self.lcd.lcd_display_string("increase privacy", 2)
            print("increase privacy")
            self.transparency.opaque()

def main():
    window = Window()
    window.lcd.lcd_display_string("starting up", 1)
    sleep(2)
    window.lcd.lcd_clear()
    window.lcd.lcd_display_string("time: ", 1)
    window.lcd.lcd_display_string("input operation mode", 2)
    while True: 
        console_input = input("operation mode number: ") 
        if console_input == "1":
            window.lcd.lcd_clear()
            window.lcd.lcd_display_string("time: ", 1)
            print("on and off mode")
            window.regular_mode()
        elif console_input == "2":
            # indicating that current state is light sensing mode
            window.lcd.lcd_clear()
            window.lcd.lcd_display_string("time: ", 1)
            window.lcd.lcd_display_string("start privacy mode", 2)
            sleep(2)
            try:
                while True:
                    sleep(0.7)
                    window.light_sensor_mode()
            except KeyboardInterrupt:
                # turn the window back to opaque
                window.lcd.lcd_display_string("time: ", 1)
                window.regular_mode()
                continue

if __name__== "__main__":
    main()
    
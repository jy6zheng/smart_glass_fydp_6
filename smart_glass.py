import time
from transparency import *
from light_sensor import *

class Window():
    def __init__(self):
        self.current_state = 0
        self.transparency = Mux()
        self.light_sensor = LightSensor()
    
    def regular_mode(self):
        if self.current_state == 0:
            self.transparency.transparent()
            self.current_state = 1
            print("turning transparent")
        else:
            self.transparency.opaque()
            self.current_state = 0
            print("turning opaque")
    
    def light_sensor_mode(self):
        difference = self.light_sensor.read_light()
        # NOTE: going to add feature that considers magnitude
        # positive indicates outside is righter
        if difference > 1:
            print("increasing privacy")
            self.transparency.transparent()
        else:
            print("increasing natural light")
            self.transparency.opaque()

def main():
    window = Window()
    
    while True:
        console_input = input("operation mode number: ")
        if console_input == "1":
            print("on and off mode")
            window.regular_mode()
        elif console_input == "2":
            # indicating that current state is light sensing mode
            window.current_state = 2
            try:
                while True:
                    time.sleep(0.7)
                    window.light_sensor_mode()
            except KeyboardInterrupt:
                # turn the window back to opaque
                window.regular_mode()
                continue

if __name__== "__main__":
    main()
    
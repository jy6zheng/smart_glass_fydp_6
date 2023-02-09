import smbus
import time

class LightSensor():
    def __init__(self):
        self.obus = smbus.SMBus(1) #outside light sensor, pins 2 and 3
        self.ibus = smbus.SMBus(3) #inside light sensor, pins 23 and 24
        self.address = 0x29
        self.obus.write_byte_data(self.address, 0x00 | 0x80, 0x03) #control register, 0x03 power on
        self.obus.write_byte_data(self.address, 0x01 | 0x80, 0x02) #timing register, 0x02 nominal  integration time 402 ms
        self.ibus.write_byte_data(self.address, 0x00 | 0x80, 0x03)
        self.ibus.write_byte_data(self.address, 0x01 | 0x80, 0x02)
    
    def read_light(self):
        odata0 = self.obus.read_i2c_block_data(self.address, 0x0c | 0x80, 2)
        odata1 = self.obus.read_i2c_block_data(self.address, 0x0e | 0x80, 2)
        idata0 = self.ibus.read_i2c_block_data(self.address, 0x0c | 0x80, 2)
        idata1 = self.ibus.read_i2c_block_data(self.address, 0x0e | 0x80, 2)
        och0 = odata0[1] * 256 + odata0[0] #IR + visible
        och1 = odata1[1] * 256 + odata1[0] #IR
        ovislight = och0 - och1 #in lux
        ich0 = idata0[1] * 256 + idata0[0] #IR + visible
        ich1 = idata1[1] * 256 + idata1[0] #IR
        ivislight = ich0 - ich1 #in lux
        
        print("outside light: %d" %ovislight)
        print("inside light: %d" %ivislight)
        return self.measure_difference(ovislight, ivislight)
    
    def measure_difference(self, ovislight, ivislight):
        # if negative, inside is brighter (opaque), if positive, outside is brighter (transparent)
        difference = ovislight - ivislight
        return difference
        
    
    
    

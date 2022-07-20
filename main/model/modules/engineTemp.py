#import Adafruit_MAX31855.MAX31855 as MAX31855

class engineTemp:

    def __init__(self):
        # Raspberry Pi software SPI configuration.
        CLK = 29
        CS = 31
        DO = 33
        global sensor 
        sensor = MAX31855.MAX31855(CLK, CS, DO)

    def getTemp():
        temp = sensor.readTempC()
        internal = sensor.readInternalC()
        return temp

import busio
import board
import digitalio
import adafruit_max31855
import time

class engineTemp:

    def __init__(self):
        cs = digitalio.DigitalInOut(board.D7)
        cs.direction = digitalio.Direction.OUTPUT
        spi = board.SPI()
        global max31855
        max31855 = adafruit_max31855.MAX31855(spi, cs)

    def getTemp(self):
        try:
         tempC = max31855.temperature 
        except:
            print("Thermocouple sensor error")
            tempC = 0
        tempC = int(((tempC-17)*100)/91)
        print("Temperature: {} C ".format(tempC))
        return tempC


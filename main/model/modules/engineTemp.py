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
        max31855 = adafruit_max31855.MAX31855(spi, cs)

    def getTemp():
        tempC = max31855.temperature 
        tempC = int(tempC-18)
        print("Temperature: {} C ".format(tempC))
        return temp

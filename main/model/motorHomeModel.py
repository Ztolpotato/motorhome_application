
#import RPi.GPIO as GPIO
#import Adafruit_GPIO.SPI as SPI
#import Adafruit_MCP3008
import time
from model.modules import coolingLevel

class Model:
    def __init__(self,controller):
        self.controller = controller
        self.coolingLevel = coolingLevel.coolingLevel()
        #GPIO.setmode (GPIO.BCM)
        #GPIO.setup (14,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #self.initMCP()

    def logicMain(self):
        while True:
            time.sleep(1)
            #self.__updateCoolantLevel()
            resistorValue = self.mcp.read_adc(0)
            print(resistorValue)

    def initMCP(self):
            # Hardware SPI configuration:
            SPI_PORT   = 0
            SPI_DEVICE = 0
            self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

    def updateCoolantLevel(self):
        state = coolingLevel.getLevel()
        if state == 1:
            self.controller.fullCoolant()
        elif state == 0:
            self.controller.moderatelyFullCoolant()
        else:
            self.controller.emptyCoolant()

    def __updateSpeed(self):
        #TODO IMPLEMENT waiting for sensors

    def __updateEngineTemperature(self):
        #TODO IMPLEMENT waiting for sensors

    def __updateFuelLevel(self):
        #TODO IMPLEMENT waiting for sensors
    
    def __updateIndoorTemperature(self):
        #TODO IMPLEMENT waiting for sensors

    def __updateOutdoorTemperature(self):
        #TODO IMPLEMENT waiting for sensors

    def __reverseSignalReceived(self):
        
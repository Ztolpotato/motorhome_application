
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import time
#from model.modules import coolingLevel
#from model.modules import fuelLevel
from model.modules import engineTemp

class Model:
    def __init__(self,controller):
        self.initMCP()
        self.controller = controller
        #self.coolingLevel = coolingLevel.coolingLevel()
        self.engineTemp = engineTemp.engineTemp()
        #self.fuelLevel = fuelLevel.fuelLevel(self.mcp)
        #GPIO.setmode (GPIO.BCM)
        #GPIO.setup (14,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        

    def logicMain(self):
        while True:
            time.sleep(4)
            self.__updateEngineTemperature()
            #self.__updateCoolantLevel()
            #self.__updateFuelLevel()
            #resistorValue = self.mcp.read_adc(0)
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
        print("not implemented yet")

    def __updateEngineTemperature(self):
        self.controller.engineTemp(self.engineTemp.getTemp())

    def __updateFuelLevel(self):
        fuelValue = self.fuelLevel.getLevel()
        if fuelValue > 75:
            self.controller.fuel100(fuelValue)
        elif fuelValue > 50 :
            self.controller.fuel50(fuelValue)
        elif fuelValue > 25 :
            self.controller.fuel25(fuelValue)
        else:
            self.controller.fuel0(fuelValue)

    def __updateIndoorTemperature(self):
        #TODO IMPLEMENT waiting for sensors
        print("not implemented yet")

    def __updateOutdoorTemperature(self):
        #TODO IMPLEMENT waiting for sensors
        print("not implemented yet")

    def __reverseSignalReceived(self):
        #TODO IMPLEMENT waiting for sensors
        print("not implemented yet")
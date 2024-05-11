
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI
import adafruit_mcp3xxx.mcp3008 as MCP
import board
import digitalio
import time
import bitbangio
import inspect
from model.modules import coolingLevel
from model.modules import temperatureSensors
from model.modules import fuelLevel
from model.modules import engineTemp
from model.modules import gps

class Model:
    def __init__(self,controller):
        #self.initMCP()
        self.controller = controller
        self.coolingLevel = coolingLevel.coolingLevel()
        self.engineTemp = engineTemp.engineTemp()
        self.allTemp = temperatureSensors.temperatureSensors()
        self.gps = gps.gps()
        #self.fuelLevel = fuelLevel.fuelLevel(self.mcp)
        GPIO.setmode(GPIO.BCM)
        global reverse
        reverse = 0
        GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        #GPIO.setup (14,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) do this on fuellevel pin

    def logicMain(self):
        self.reverse = GPIO.input(11)
        while True:
            self.__updateEngineTemperature()
            self.__updateAlltemperatures()
            time.sleep(1)
            self.__updateCoolantLevel()
            self.__updateGPS()
            if GPIO.input(11) != self.reverse:
                self.reverse = GPIO.input(11)
                #HERE WE CHANGE BETWEEN SCREENS
            #self.__updateFuelLevel()
            #resistorValue = self.mcp.read_adc(0)
            #print(resistorValue)

    def initMCP(self):
            cs = digitalio.DigitalInOut(board.D29)
            #cs.direction = digitalio.Direction.OUTPUT
            #cs.value = True
            #spi = bitbangio.SPI(board.D33, MISO=board.D31,MOSI=board.D35)
            # Hardware SPI configuration:
            #SPI_PORT   = 0
            #SPI_DEVICE = 0
            #spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE)
            #self.mcp = MCP.MCP3008(spi)
    def __updateGPS(self):
        speed = self.gps.getSpeed()
        self.controller.setSpeed(speed)

    def __updateCoolantLevel(self):
        state = self.coolingLevel.getLevel()
        if state == 1:
            self.controller.fullCoolant()
        elif state == 0:
            self.controller.moderatelyFullCoolant()
        else:
            self.controller.emptyCoolant()

    def __updateEngineTemperature(self):
        self.controller.engineTemp(self.engineTemp.getTemp())

    def __updateAlltemperatures(self):
        self.controller.updateAllTemps(self.allTemp.read_temp('outdoor'),self.allTemp.read_temp('indoor'))

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

    def __reverseSignalReceived(self):
        #TODO IMPLEMENT waiting for sensors
        print("not implemented yet")

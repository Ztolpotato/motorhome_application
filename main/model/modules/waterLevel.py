import RPi.GPIO as GPIO

class fluidLevel:

    def __init__(self):
        self.slidingWindowWaterTank = []
        self.slidingWindowBrownTank = []
        self.slidingWindowBlackTank = []
        self.waterHigh = 21
        self.waterMedium = 20
        self.waterLow = 19
        self.blackWaterHigh = 27
        self.blackWaterLow = 26
        self.brownWaterHigh = 6
        self.brownWaterLow = 5
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(21,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(20,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(19,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(27,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(26,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(6,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(5,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    #Returns 0-3 for watertank and 0-2 for grey and blackwater
    def getLevel(self):
        waterTank = 0
        greyWaterTank = 0
        blackWaterTank = 0
        self.slidingWindowWaterTank.insert(0, GPIO.input(self.waterHigh) +  GPIO.input(self.waterMedium) +  GPIO.input(self.waterLow))
        if len(self.slidingWindowWaterTank) > 10:
           self.slidingWindowWaterTank.pop()
           watertank = sum(self.slidingWindowWaterTank)//10
        self.slidingWindowBrownTank.insert(0, GPIO.input(self.brownWaterHigh) + GPIO.input(self.brownWaterLow))
        if len(self.slidingWindowBrownTank) > 10:
           self.slidingWindowBrownTank.pop()
           greyWaterTank = sum(self.slidingWindowBrownTank)//10
        self.slidingWindowBlackTank.insert(0, GPIO.input(self.blackWaterHigh) + GPIO.input(self.blackWaterLow))
        if len(self.slidingWindowBlackTank) > 10:
           self.slidingWindowBlackTank.pop()
           blackWaterTank = sum(self.slidingWindowBlackTank)//10
        return (waterTank, greyWaterTank, blackWaterTank)

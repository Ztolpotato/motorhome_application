import RPi.GPIO as GPIO

class coolingLevel:

    def __init__(self):
        self.slidingWindow = []
        self.high = 24
        self.low = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(24,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(23,GPIO.IN, pull_up_down=GPIO.PUD_DOWN) 
    #Returns -1 if level is to low, 0 if above lowest or 1 if full
    def getLevel(self):
        lowState = GPIO.input(self.low)
        highState = GPIO.input(self.high)

        self.slidingWindow.insert(0,lowState+highState)

        if len(self.slidingWindow) > 11:
            self.slidingWindow.pop()
            self.slidingWindow.pop()

        i = sum(self.slidingWindow)
        #print(self.slidingWindow)
        #print(lowState)
        #print(highState)
        if len(self.slidingWindow) > 5:
            if i > 15:
                return 1
            elif i > 9:
                return 0
            else:
                return -1
        currentVolumeReading = lowState + highState
        if currentVolumeReading == 2:
            return 1
        elif currentVolumeReading == 1:
            return 0
        else:
            return -1

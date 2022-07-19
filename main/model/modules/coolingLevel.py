#import RPi.GPIO as GPIO

class coolingLevel:

    def __init__(self):
        self.slidingWindow = []
        self.high = 24
        self.low = 23

    #Returns -1 if level is to low, 0 if above lowest or 1 if full
    def getLevel():
        lowState = GPIO.input(self.low)
        highState = GPIO.input(self.high)
        self.slidingWindow.append(lowState)
        self.slidingWindow.append(highState+1)
        if self.slidingWindow.qsize() > 21:
            self.slidingWindow.pop()
            self.slidingWindow.pop()
        i = sum(queue)
        if self.slidingWindow.qsize() > 15:
            if i > 30:
                return 1
            elif i > 12:
                return 0
            else:
                return -1
        currentVolumeReading = lowState + highState
        if currentVolumeReading == 3:
            return 1
        elif currentVolumeReading == 1:
            return 0
        else:
            return -1
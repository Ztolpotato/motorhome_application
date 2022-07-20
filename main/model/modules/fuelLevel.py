class fuelLevel:

    def __init__(self,mcp):
        self.slidingWindow = []
        self.mcp = mcp


    #Returns percentage value of fuel
    def getLevel():
        fuelSampleValue = self.mcp.read_adc(0)
        self.slidingWindow.append(fuelSampleValue)
        if self.slidingWindow.qsize() > 20:
            self.slidingWindow.pop()
        i = sum(queue)
        #TODO add logic to return percentage of fuel left in tank
        return i
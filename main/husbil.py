from gui import sensorWindow
from gui import reversingCamera
from gui import startPage
from gui import engineSensorsWindow
from model import motorHomeModel

import bitbangio
import board
import digitalio
import adafruit_max31855

#from controller import motorHomeController
import tkinter as tk
import threading

class MotorHomeApplication(tk.Tk):
    
    
    def __init__(self):
        super().__init__()
        self.title("MotorHome sensor and reversing camera application")
        #Set the Geometry
        self.geometry("800x480")
        container = tk.Frame(background="#1E2130")
        container.pack(side="bottom", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.pack()
        self['bg'] = "#1E2130"
        
        #Full Screen Window
        #self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        

        #Creates frames and saves them in self.frames
        #Change which frame is on top with show_frame
        self.frames = {}
        for F in (startPage.startPage,sensorWindow.sensorWindow, reversingCamera.reversingCamera,
        engineSensorsWindow.engineSensorsWindow):
            page_name = F.__name__
            frame = F(parent=container)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame("startPage")
        self.sensorView = self.frames["sensorWindow"]
        self.engineSensorView = self.frames["engineSensorsWindow"]
        self.reversingCameraView = self.frames["reversingCamera"]

        self.mod = motorHomeModel.Model(self)
        self.engineSensorView.set_controller(self)
        self.sensorView.set_controller(self)
        self.reversingCameraView.set_controller(self)
        
        th = threading.Thread(target=self.mod.logicMain)
        th.start()
        th2 = threading.Thread(target=self.th_camera)
        th2.start()
        self.show_frame("reversingCamera")
        #self.engineSensorView.updateEngineTemp(75)
        #self.engineSensorView.emptyCoolant()
        #self.engineSensorView.fuel0("12")
    def th_camera(self):
        # Raspberry Pi software SPI configuration.
        CLK = 13
        CS  = 19
        DO  = 26
        cs = digitalio.DigitalInOut(board.D19)
        cs.direction = digitalio.Direction.OUTPUT
        cs.value = True
        spi.configure(baudrate=5000000, phase=0, polarity=0)
        spi = bitbangio.SPI(board.D13,MISO=board.D26)
        max31855 = adafruit_max31855.MAX31855(spi, cs)
        while True:
            tempC = max31855.temperature
            tempF = tempC * 9 / 5 + 32
            print("Temperature: {} C {} F ".format(tempC, tempF))
            time.sleep(2.0)
        #self.reversingCameraView.runVideoStream()

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()

    def fullCoolant():
        self.engineSensorView.fullCoolant()

    def moderatelyFullCoolant():
        self.engineSensorView.moderateCoolant()

    def emptyCoolant():
        self.engineSensorView.emptyCoolant()

    def fuel100(fuelValue):
        self.engineSensorView.fuel100(fuelValue)

    def fuel50(fuelValue):
        self.engineSensorView.fuel50(fuelValue)

    def fuel25(fuelValue):
        self.engineSensorView.fuel25(fuelValue)

    def fuel0(fuelValue):
        self.engineSensorView.fuel0(fuelValue)

    def engineTemp(engineTemp):
        self.engineSensorView.updateEngineTemp(engineTemp)

if __name__ == '__main__':
    app =  MotorHomeApplication()
    app.mainloop()


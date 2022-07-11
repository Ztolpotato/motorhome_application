from gui import sensorWindow
from gui import reversingCamera
from gui import startPage
from gui import engineSensorsWindow
from model import motorHomeModel
from controller import motorHomeController
import tkinter as tk
import dash_daq as dash
from dash import dcc
import time
from dash import html
import threading
#from tkhtmlview import HTMLLabel
#from PIL import ImageTk, Image
import RPi.GPIO as GPIO

class MotorHomeApplication(tk.Tk):
    
    
    def __init__(self):
        super().__init__()
        print("Starting...")
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
        self.attributes('-fullscreen', True)
        self.bind("<Escape>", lambda event: self.attributes("-fullscreen", False))
        
        self.frames = {}
        for F in (startPage.startPage,sensorWindow.sensorWindow, reversingCamera.reversingCamera,
        engineSensorsWindow.engineSensorsWindow):
            page_name = F.__name__
            frame = F(parent=container)
            self.frames[page_name] = frame
            print(frame)

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")
        self.sensorView = self.frames["sensorWindow"]
        self.engineSensorView = self.frames["engineSensorsWindow"]
        reversingCameraView = self.frames["reversingCamera"]

        mod = motorHomeModel.Model("df")
        controller = motorHomeController.Controller(self.sensorView,mod)
        self.engineSensorView.set_controller(self)
        self.sensorView.set_controller(self)
        self.show_frame("sensorWindow")
        GPIO.setmode (GPIO.BCM)
        GPIO.setup (14,GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        th = threading.Thread(target=self.threadFunc)
        th.start()
        print("bullcrap")
        

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
    
    def changePic(self):
        self.engineSensorView.empty()
        
    def threadFunc(self):
        while True:
            time.sleep(1)
            
            state = GPIO.input(14)
            print(state)
            if state is 1:
                print("somtimes full")
                self.engineSensorView.fullFuel()
            else:
                self.engineSensorView.empty()


if __name__ == '__main__':
    app =  MotorHomeApplication()
    app.mainloop()


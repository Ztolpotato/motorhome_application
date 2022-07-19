from gui import sensorWindow
from gui import reversingCamera
from gui import startPage
from gui import engineSensorsWindow
from model import motorHomeModel

#from controller import motorHomeController
import tkinter as tk
import dash_daq as dash
from dash import dcc
from dash import html
import threading

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
        self.sensorView = self.frames["sensorWindow"]
        self.engineSensorView = self.frames["engineSensorsWindow"]
        reversingCameraView = self.frames["reversingCamera"]

        self.mod = motorHomeModel.Model(self)
        self.engineSensorView.set_controller(self)
        self.sensorView.set_controller(self)
        self.show_frame("sensorWindow")
        th = threading.Thread(target=self.mod.logicMain)
        th.start()
        

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

if __name__ == '__main__':
    app =  MotorHomeApplication()
    app.mainloop()


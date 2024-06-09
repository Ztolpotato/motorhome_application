import tkinter as tk
from tkinter import ttk
from plotly import graph_objects as go
from PIL import ImageTk, Image
import numpy as np
import cv2
class sensorWindow(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #self = parent
        self.grid()
        self.controller = None
        #self.__setEngineTemp()
        #self.__setCoolantLevel()
        #self.__setFuelLevel()
        self.__setWaterLevel("fluid50.png")
        self.__setGreyWaterLevel("fluid50GT.png")
        self.__setBlackWaterLevel("fluid50GT.png")
        self.setOutdoorTemperature()
        self.setBatteryLevel()
        self.setIndoorTemperature()
        temp = tk.Label(self,text="", bg="#1E2130",pady=20)
        temp.grid(row=5,column=0)
        self.addFrameSwitchButton()

    def addFrameSwitchButton(self):
        switchButton = tk.Button(self,text="Engine Screen",fg='white', bg="#1E2130", font=("Open sans", 15),
                command=self.onSwitchButtonClick)
        switchButton.grid(row=6,column=0)
        switchButton.grid_columnconfigure(1,weight=1)
        switchButton.grid_rowconfigure(1,weight=1)
    def onSwitchButtonClick(self):
        self.controller.show_frame("engineSensorsWindow")

    def set_controller(self,controller):
        self.controller = controller

    def setLevels(self, levels):
        self.__waterSwitch(levels[0])
        self.__greyWaterSwitch(levels[1])
        self.__blackWaterSwitch(levels[2])

    def __waterSwitch(self, level):
        if level == 0:
            self.__setWaterLevel("coolantLow.png")
        elif level == 1:
            self.__setWaterLevel("fluid50.png")
        elif level == 2:
            self.__setWaterLevel("fluid50.png")
        elif level == 3:
            self.__setWaterLevel("coolantHigh.png")

    def __greyWaterSwitch(self, level):
        if level == 0:
            self.__setGreyWaterLevel("coolantLow.png")
        elif level == 1:
            self.__setGreyWaterLevel("fluid50GT.png")
        elif level == 2:
            self.__setGreyWaterLevel("coolantHigh.png")

    def __blackWaterSwitch(self, level):
        if level == 0:
            self.__setBlackWaterLevel("coolantLow.png")
        elif level == 1:
            self.__setBlackWaterLevel("fluid50GT.png")
        elif level == 2:
            self.__setBlackWaterLevel("coolantHigh.png")

    def setBatteryLevel(self):
        self.__addText("Battery voltage" + " - V", 2, 0, 2)

    def setOutdoorTemperature(self):
        self.__addText("Outdoor Temp: " + "- C\N{DEGREE SIGN}", 3, 0, 1)

    def setIndoorTemperature(self):
        self.__addText("Indoor Temp: " + "- C\N{DEGREE SIGN}", 4, 0, 1)

    def __setBlackWaterLevel(self, image):
        global blackWaterImg
        blackWaterImg = ImageTk.PhotoImage(Image.open(image))
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=2, column=3)
        #canvas.pack()
        canvas.create_image(100,150, anchor="s",image=blackWaterImg)
        self.__addTitleToImage("Blackwater level", 1, 3)


    def __setGreyWaterLevel(self, image):
        global greeyWaterImg
        greeyWaterImg = ImageTk.PhotoImage(Image.open(image))
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=4, column=3)
        #canvas.pack()
        canvas.create_image(100,150, anchor="s",image=greeyWaterImg)
        self.__addTitleToImage("Greywater level", 3, 3)

    def __setWaterLevel(self, image):
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=4, column=2)
        global img 
        img = ImageTk.PhotoImage(Image.open(image))
        temp = canvas.create_image(100,150, anchor="s",image=img)
        self.__addTitleToImage("Water level", 3, 2)

    def __addTitleToImage(self,text,row,col):
        label = tk.Label(self,text=text,bg="#1E2130",fg='white',font=("Open sans", 15))
        label.grid(row=row,column=col)

    def __addText(self,text,row,col,span):
        label = tk.Label(self,text=text,bg="#1E2130",fg='white',font=("Open sans", 15))
        label.grid(row=row,column=col,rowspan=span)

    def __createFigure(self):
        lay = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = 50,
            mode = "gauge+number",
            #title = {'text': "Engine temperature", 'font':{'color':"White", 'size': 50}},
            gauge = {'axis': {'range': [-20, 120], 'tickwidth': 1,'tickcolor': "black"},
                'bar': {'color': "MidnightBlue"},
                    'steps' : [
                        {'range': [-20, 40], 'color': "Blue"},
                        {'range': [40, 80], 'color': "Green"},
                        {'range': [80, 95], 'color': "Orange"},
                        {'range': [95, 120], 'color': "Red"}]}),layout=lay)
        return fig

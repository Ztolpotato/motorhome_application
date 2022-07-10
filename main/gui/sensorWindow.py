import tkinter as tk
from tkinter import ttk
import plotly.graph_objects as go
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
        self.__setWaterLevel()
        self.__setGreyWaterLevel()
        self.__setBlackWaterLevel()
        self.setOutdoorTemperature()
        self.setBatteryLevel()
        self.setIndoorTemperature()
        temp = tk.Label(self,text="", bg="#1E2130",pady=20)
        temp.grid(row=5,column=0)
        self.addFrameSwitchButton()

    def addFrameSwitchButton(self):
        switchButton = tk.Button(self,text="Switch Screen",fg='white', bg="#1E2130", font=("Open sans", 15),
                command=self.onSwitchButtonClick)
        switchButton.grid(row=6,column=0)
        switchButton.grid_columnconfigure(1,weight=1)
        switchButton.grid_rowconfigure(1,weight=1)
    def onSwitchButtonClick(self):
        self.controller.show_frame("engineSensorsWindow")

    def set_controller(self,controller):
        self.controller = controller

    def setBatteryLevel(self):
        self.__addText("Battery voltage" + " - V", 2, 0, 2)

    def setOutdoorTemperature(self):
        self.__addText("Outdoor Temp: " + "- C\N{DEGREE SIGN}", 3, 0, 1)

    def setIndoorTemperature(self):
        self.__addText("Indoor Temp: " + "- C\N{DEGREE SIGN}", 4, 0, 1)

    def __setBlackWaterLevel(self):
        global blackWaterImg
        blackWaterImg = ImageTk.PhotoImage(Image.open("fluid50GT.png"))
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=2, column=3)
        #canvas.pack()
        canvas.create_image(100,150, anchor="s",image=blackWaterImg)
        self.__addTitleToImage("Greywater level", 1, 3)


    def __setGreyWaterLevel(self):
        global greeyWaterImg
        greeyWaterImg = ImageTk.PhotoImage(Image.open("fluid50GT.png"))
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=4, column=3)
        #canvas.pack()
        canvas.create_image(100,150, anchor="s",image=greeyWaterImg)
        self.__addTitleToImage("Greywater level", 3, 3)

    def __setWaterLevel(self):
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=4, column=2)
        global img 
        img = ImageTk.PhotoImage(Image.open("fluid50T.png"))
        temp = canvas.create_image(100,150, anchor="s",image=img)
        self.__addTitleToImage("Water level", 3, 2)

    def __setFuelLevel(self):
        global fuelImg
        fuelImg = ImageTk.PhotoImage(Image.open("fluid50DT.png"))
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=4, column=1)
        #canvas.pack()
        canvas.create_image(100,150, anchor="s",image=fuelImg)
        self.__addTitleToImage("Fuel level", 3, 1)

    def __setCoolantLevel(self):
        global CoolantImg
        CoolantImg = ImageTk.PhotoImage(Image.open("fluid50T.png"))
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=4, column=0)
        #canvas.pack()
        canvas.create_image(100,150, anchor="s",image=CoolantImg)
        self.__addTitleToImage("Coolant level", 3, 0)

    def __addTitleToImage(self,text,row,col):
        label = tk.Label(self,text=text,bg="#1E2130",fg='white',font=("Open sans", 15))
        label.grid(row=row,column=col)

    def __addText(self,text,row,col,span):
        label = tk.Label(self,text=text,bg="#1E2130",fg='white',font=("Open sans", 15))
        label.grid(row=row,column=col,rowspan=span)


    def __setEngineTemp(self):
        global tempImg
        tempImg = Image.open("gauge.png")
        tempImg = ImageTk.PhotoImage(tempImg)
        canvas = tk.Canvas(self, bg="#1E2130", width=210, height=100,highlightthickness=0)
        canvas.grid(row=1, column=0)
        canvas.create_image(100,115, anchor="s",image=tempImg)
        self.__addTitleToImage("Engine temperature", 0, 0)

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
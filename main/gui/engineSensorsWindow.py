import tkinter as tk
from tkdial import Meter
from tkinter import ttk
from tkinter import StringVar
import plotly.graph_objects as go
from PIL import ImageTk, Image
import numpy as np
import cv2
import io

class engineSensorsWindow(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.grid()
        self.controller = None
        self.__initiateEngineTemperature(1,0,1,1)
        self.__InitiateCoolantLevel(1,1,1,1)
        self.__setFuelLevel(3,1,1,1)
        self.__setSpeedometer(3, 0, 1, 1)
        self.__addFrameSwitchButton(4)
        self.__addCameraButton(4)
        self.__setOutdoorTemperature(1,2,1,1)
        self.__setIndoorTemperature(3,2,1,1)
        self.__setFuelPercentageValue(2,2,1,1)
        for row in range(5):
            self.grid_rowconfigure(row, weight=1)
        for col in range(2):
            self.grid_columnconfigure(col, weight=1)
        global emptyFuel
        emptyFuel = ImageTk.PhotoImage(Image.open("fluid0T.png"))
        global speedfig

    def __initiateEngineTemperature(self,row,col,rowspan,colspan):
        global meter2
        meter2 = Meter(self, radius=200, start=0, end=120, border_width=0,
               fg="#1E2130", text_color="white", start_angle=270, end_angle=-270,
               text_font="DS-Digital 30", scale_color="white", needle_color="red", bg="#1E2130",)
        meter2.set_mark(85, 120) # set red marking from 140 to 160
        meter2.set(0)
        meter2.grid(row=row, column=col, padx=rowspan, pady=colspan)

    def set_controller(self,controller):
        self.controller = controller

    def __setFuelPercentageValue(self,row,col,rowspan,colspan):
        global fuelText
        fuelText = tk.StringVar()
        fuelText.set("Fuel: - %")
        fuelPercentageLabel = tk.Label(self,textvariable=fuelText,bg="#1E2130",fg='white',font=("Open sans", 15))
        fuelPercentageLabel.grid(row=row,column=col,rowspan=rowspan)

    def __setOutdoorTemperature(self,row,col,rowspan,colspan):
        global outdoortemp
        outdoortemp = tk.StringVar()
        outdoortemp.set("Outdoor Temp: " + " -C\N{DEGREE SIGN}")
        outdoortempLabel = tk.Label(self,textvariable=outdoortemp,bg="#1E2130",fg='white',font=("Open sans", 15))
        outdoortempLabel.grid(row=row,column=col,rowspan=rowspan)

    def __setIndoorTemperature(self,row,col,rowspan,colspan):
        global indoortemp
        indoortemp = tk.StringVar()
        indoortemp.set("Outdoor Temp: " + " -C\N{DEGREE SIGN}")
        indoortempLabel = tk.Label(self,textvariable=indoortemp,bg="#1E2130",fg='white',font=("Open sans", 15))
        indoortempLabel.grid(row=row,column=col,rowspan=rowspan)

    def __addFrameSwitchButton(self,row):
        switchButton = tk.Button(self,text="Sensor screen",fg='white', bg="#1E2130", font=("Open sans", 15),
                command=self.onSwitchButtonClick)
        switchButton.grid(row=row,column=0)

    def __addCameraButton(self,row):
        reversingButton = tk.Button(self,text="Reversing Camera",fg='white', bg="#1E2130", font=("Open sans", 15),
                command=self.onCameraButtonClick)
        reversingButton.grid(row=row,column=1)

    def onSwitchButtonClick(self):
        self.controller.show_frame("sensorWindow")

    def onCameraButtonClick(self):
        self.controller.show_frame("reversingCamera")

    def __setFuelLevel(self,row,col,rowspan,colspan):
        global fuelImg
        fuelImg = ImageTk.PhotoImage(Image.open("fuel_100_percent.png"))
        global fuelCanvas
        fuelCanvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        fuelCanvas.grid(row=row, column=col,rowspan=rowspan,columnspan=colspan)
        global fuelCImg
        fuelCImg = fuelCanvas.create_image(100,150, anchor="s",image=fuelImg)
        self.__addTitleToImage("Fuel level", row-1, col)

    def __InitiateCoolantLevel(self,row,col,rowspan,colspan):
        global CoolantImg
        CoolantImg = ImageTk.PhotoImage(Image.open("water_100_percent.png"))
        global coolantCanvas
        coolantCanvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        coolantCanvas.grid(row=row, column=col,rowspan=rowspan,columnspan=colspan)
        global coolantContainer
        coolantContainer = coolantCanvas.create_image(100,150, anchor="s",image=CoolantImg)
        self.__addTitleToImage("Coolant level", row-1, col)

    def __addTitleToImage(self,text,row,col):
        label = tk.Label(self,text=text,bg="#1E2130",fg='white',font=("Open sans", 15))
        label.grid(row=row,column=col,sticky="s")

    def __setSpeedometer(self,row,col,rowspan,colspan):
        global speed 
        speed = StringVar()
        speed.set("0")
        label = tk.Label(self,textvariable=speed,bg="#1E2130",fg="White" ,font=("Open sans", 80))
        label.grid(row=row, column=col,columnspan=colspan,rowspan=rowspan)

    def __setFuel(self,image):
        fuelImg = Image.open(image)
        fuelImg = ImageTk.PhotoImage(fuelImg)
        fuelCanvas.imgref = fuelImg
        fuelCanvas.itemconfig(fuelCImg,image = fuelImg)

    def __setCoolantLevel(self, image):
        CoolantImg = Image.open(image)
        CoolantImg = ImageTk.PhotoImage(CoolantImg)
        coolantCanvas.imgref = CoolantImg
        coolantCanvas.itemconfig(fuelCImg,image = CoolantImg)

    def updateFuelLevel(self, level):
        if level < 2:
            self.__setFuel("fuel_0_percent.png")
        elif level > 8:
            self.__setFuel("fuel_100_percent.png")
        else:
            self.__setFuel("fuel_50_percent.png")

    def updateCoolantLevel(self, level):
        if level == 1:
            self.__setCoolantLevel("water_50_percent.png")
        elif level == 2:
            self.__setCoolantLevel("water_100_percent.png")
        else:
            self.__setCoolantLevel("water_0_percent.png")

    def updateEngineTemp(self,engineTemp):
        meter2.set(str(engineTemp))

    def updateAllTemps(self,outdoor,indoor):
        outdoortemp.set("Outdoor Temp: " + "{:.1f}".format(outdoor) +" C\N{DEGREE SIGN}")
        indoortemp.set("Indoor Temp: " + "{:.1f}".format(indoor) +" C\N{DEGREE SIGN}")

    def setSpeed(self,speed):
        speed.set(str(speed))


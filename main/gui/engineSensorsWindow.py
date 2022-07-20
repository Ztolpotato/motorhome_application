import tkinter as tk
from tkinter import ttk
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
        self.__setEngineTemp(1,0,1,1)
        self.__setCoolantLevel(1,1,1,1)
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
        

    def set_controller(self,controller):
        self.controller = controller

    def __setFuelPercentageValue(self,row,col,rowspan,colspan):
        global fuelText
        fuelText = tk.StringVar()
        fuelText.set("Fuel: - %")
        fuelPercentageLabel = tk.Label(self,textvariable=fuelText,bg="#1E2130",fg='white',font=("Open sans", 15))
        fuelPercentageLabel.grid(row=row,column=col,rowspan=rowspan)

    def __setOutdoorTemperature(self,row,col,rowspan,colspan):
        self.__addText("Outdoor Temp: " + "- C\N{DEGREE SIGN}", row, col, rowspan)

    def __setIndoorTemperature(self,row,col,rowspan,colspan):
        self.__addText("Indoor Temp: " + "- C\N{DEGREE SIGN}", row, col, rowspan)

    def __addText(self,text,row,col,span):
        label = tk.Label(self,text=text,bg="#1E2130",fg='white',font=("Open sans", 15))
        label.grid(row=row,column=col,rowspan=span)

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
        fuelImg = ImageTk.PhotoImage(Image.open("fluid50DT.png"))
        global fuelCanvas
        fuelCanvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        fuelCanvas.grid(row=row, column=col,rowspan=rowspan,columnspan=colspan)
        global fuelCImg
        fuelCImg = fuelCanvas.create_image(100,150, anchor="s",image=fuelImg)
        self.__addTitleToImage("Fuel level", row-1, col)

    def __setCoolantLevel(self,row,col,rowspan,colspan):
        global CoolantImg
        CoolantImg = ImageTk.PhotoImage(Image.open("fluid50T.png"))
        global coolantCanvas
        coolantCanvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        coolantCanvas.grid(row=row, column=col,rowspan=rowspan,columnspan=colspan)
        global coolantContainer
        coolantContainer = coolantCanvas.create_image(100,150, anchor="s",image=CoolantImg)
        self.__addTitleToImage("Coolant level", row-1, col)

    def __addTitleToImage(self,text,row,col):
        label = tk.Label(self,text=text,bg="#1E2130",fg='white',font=("Open sans", 15))
        label.grid(row=row,column=col,sticky="s")

    def __setEngineTemp(self,row,col,rowspan,colspan):
        speedometer = self.__createFigure(0)
        speedometer.write_image("assets/temp.png")
        engineTempImg = Image.open("assets/temp.png")
        engineTempImg = engineTempImg.resize((210,150))
        engineTempImg = ImageTk.PhotoImage(engineTempImg)
        global engineCanvas
        engineCanvas = tk.Canvas(self, bg="#1E2130", width=210, height=100,highlightthickness=0)
        engineCanvas.grid(row=row, column=col,columnspan=colspan,rowspan=rowspan)
        engineCanvas.create_image(100,115, anchor="s",image=engineTempImg)
        engineCanvas.imgref = engineTempImg
        self.__addTitleToImage("Engine temperature", row-1, col)

    def __setSpeedometer(self,row,col,rowspan,colspan):
        global speedometer
        speedometer = self.__createSpeedGaugeFigure(0)
        speedometer.write_image("speed.png")
        global img
        img = Image.open("speed.png")
        img = img.resize((210,150))
        img = ImageTk.PhotoImage(img)
        
        canvas = tk.Canvas(self, bg="#1E2130", width=210, height=150,highlightthickness=0)
        canvas.grid(row=row, column=col,columnspan=colspan,rowspan=rowspan)
        canvas.create_image(100,115, anchor="s",image=img)
        canvas.imgref = img
        self.__addTitleToImage("SPEED", row-1, col)

    def __createFigure(self,temp):
        lay = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        fig = go.Figure(go.Indicator(
            domain = {'x': [0, 1], 'y': [0, 1]},
            value = temp,
            mode = "gauge+number",
            number = {'font': {'size': 150}},
            gauge = {'axis': {'range': [-20, 120], 'tickwidth': 1,'tickcolor': "black"},
                'bar': {'color': "MidnightBlue"},#MidnightBlue"},
                    'steps' : [
                        {'range': [-20, 40], 'color': "Blue"},
                        {'range': [40, 80], 'color': "Green"},
                        {'range': [80, 95], 'color': "Orange"},
                        {'range': [95, 120], 'color': "Red"}]}),
                        layout=lay)
        return fig

    def __createSpeedGaugeFigure(self,speed):
        lay = go.Layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        speedfig = go.Figure(go.Indicator(
            mode = "number",
            value = speed,
            number= {'font': {'size': 150}},
            domain = {'row': 0, 'column': 1},
            #domain = {'x': [0, 1], 'y': [0, 1]},
            #gauge = {'axis': {'range': [None, 160]}}
            ),
            layout=lay)
        return speedfig

    def fuel100(self,fuelValue):
        fuelImg = Image.open("fluid50DT.png")
        fuelImg = ImageTk.PhotoImage(fuelImg)
        fuelCanvas.imgref = fuelImg
        fuelCanvas.itemconfig(fuelCImg,image = fuelImg)
        self.changeFuelText(fuelValue)

    def fuel50(self,fuelValue):
        fuelImg = Image.open("fluid50DT.png")
        fuelImg = ImageTk.PhotoImage(fuelImg)
        fuelCanvas.imgref = fuelImg
        fuelCanvas.itemconfig(fuelCImg,image = fuelImg)
        self.changeFuelText(fuelValue)

    def fuel25(self,fuelValue):
        fuelImg = Image.open("fluid50DT.png")
        fuelImg = ImageTk.PhotoImage(fuelImg)
        fuelCanvas.imgref = fuelImg
        fuelCanvas.itemconfig(fuelCImg,image = fuelImg)
        self.changeFuelText(fuelValue)

    def fuel0(self,fuelValue):
        fuelImg = Image.open("fluid0DT.png")
        fuelImg = ImageTk.PhotoImage(fuelImg)
        fuelCanvas.imgref = fuelImg
        fuelCanvas.itemconfig(fuelCImg,image = fuelImg)
        self.changeFuelText(fuelValue)

    def changeFuelText(self,fuelvalue):
        fuelText.set("Fuel: " + fuelvalue + "%")

    def empty(self):
        emptyFuel = Image.open("fluid0T.png")
        emptyFuel = ImageTk.PhotoImage(emptyFuel)
        fuelCanvas.imgref = emptyFuel
        fuelCanvas.itemconfig(fuelCImg,image = emptyFuel)

    def fullCoolant(self):
        fullCoolant = Image.open("coolantHigh.png")
        fullCoolant = ImageTk.PhotoImage(fullCoolant)
        coolantCanvas.imgref = fullCoolant
        coolantCanvas.itemconfig(coolantContainer,image = fullCoolant)

    def emptyCoolant(self):
        emptyCoolant = Image.open("coolantLow.png")
        emptyCoolant = ImageTk.PhotoImage(emptyCoolant)
        coolantCanvas.imgref = emptyCoolant
        coolantCanvas.itemconfig(coolantContainer,image = emptyCoolant)

    def moderateCoolant(self):
        moderateCoolant = Image.open("fluidOKT.png")
        moderateCoolant = ImageTk.PhotoImage(moderateCoolant)
        coolantCanvas.imgref = moderateCoolant
        coolantCanvas.itemconfig(coolantContainer,image = moderateCoolant)

    def updateEngineTemp(self,engineTemp):
        speedometer = self.__createFigure(engineTemp)
        speedometer.write_image("assets/temp.png")
        engineTempImg = Image.open("assets/temp.png")
        engineTempImg = engineTempImg.resize((210,150))
        engineTempImg = ImageTk.PhotoImage(engineTempImg)
        engineCanvas.imgref = engineTempImg
        engineCanvas.itemconfig(fuelCImg,image = engineTempImg)
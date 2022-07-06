import tkinter as tk
from tkinter import ttk
import plotly.graph_objects as go
from PIL import ImageTk, Image
import numpy as np
import cv2

class engineSensorsWindow(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        #self = parent
        self.grid()
        self.controller = None
        self.__setEngineTemp()
        self.__setCoolantLevel()
        self.__setFuelLevel()
        self.addFrameSwitchButton()
        for row in range(3):
            self.grid_rowconfigure(row, weight=1)
        for col in range(2):
            self.grid_columnconfigure(col, weight=1)

    def set_controller(self,controller):
        self.controller = controller

    def addFrameSwitchButton(self):
        switchButton = tk.Button(self,text="Switch Screen",fg='white', bg="#1E2130", font=("Open sans", 12),
                command=self.onSwitchButtonClick)
        switchButton.grid(row=3,column=0)

    def onSwitchButtonClick(self):
        self.controller.show_frame("sensorWindow")
    
    def __setFuelLevel(self):
        global fuelImg
        fuelImg = ImageTk.PhotoImage(Image.open("fluid50DT.png"))
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=1, column=1)
        #canvas.pack()
        canvas.create_image(100,150, anchor="s",image=fuelImg)
        self.__addTitleToImage("Fuel level", 0, 1)

    def __setCoolantLevel(self):
        global CoolantImg
        CoolantImg = ImageTk.PhotoImage(Image.open("fluid50T.png"))
        canvas = tk.Canvas(self, bg="#1E2130", width=190, height=150,highlightthickness=0)
        canvas.grid(row=1, column=2)
        #canvas.pack()
        canvas.create_image(100,150, anchor="s",image=CoolantImg)
        self.__addTitleToImage("Coolant level", 0, 2)

    def __addTitleToImage(self,text,row,col):
        label = tk.Label(self,text=text,bg="#1E2130",fg='white',font=("Open sans", 12))
        label.grid(row=row,column=col,sticky="s")

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
            gauge = {'axis': {'range': [-20, 120], 'tickwidth': 1,'tickcolor': "black"},
                'bar': {'color': "MidnightBlue"},
                    'steps' : [
                        {'range': [-20, 40], 'color': "Blue"},
                        {'range': [40, 80], 'color': "Green"},
                        {'range': [80, 95], 'color': "Orange"},
                        {'range': [95, 120], 'color': "Red"}]}),layout=lay)
        return fig
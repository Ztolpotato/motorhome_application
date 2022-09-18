import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import cv2
class reversingCamera(tk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.controller = None
        # Initialize style
        s = ttk.Style()
        global cap
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        # Create style used by default for all Frames
        s.configure('TFrame', background="#1E2130")
        self.lmain = tk.Label(self, borderwidth=0)
        self.lmain.grid()
        self.__addFrameSwitchButton()
        #self.setVideoStreamDevice(0)

    def set_controller(self,controller):
        self.controller = controller

    def __addFrameSwitchButton(self):
        global backButton
        backButton = tk.PhotoImage(file= r'assets/BackButton.png')
        backButton = backButton.subsample(30, 30)
        switchButton = tk.Button(self,text="Switch Screen",fg='black', image=backButton, bg="white", font=("Open sans", 15),
                command=self.onSwitchButtonClick)
        switchButton.grid(row=0,column=0)

    def onSwitchButtonClick(self):
        self.controller.show_frame("engineSensorsWindow")

    def runVideoStream(self):
        try:
            ret, frame = cap.read()
            if ret==True:
                frame = cv2.resize(frame,(800,450),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                img = Image.fromarray(cv2image)
                imgtk = ImageTk.PhotoImage(image=img)
                self.lmain.imgtk = imgtk
                self.lmain.configure(image=imgtk)
            self.lmain.after(1, self.runVideoStream)
        except:
            print("Failed to access camera feed")

    def releaseVideoStream():
        cap.release()

    def setVideoStreamDevice(self,device):
        cap = cv2.VideoCapture(device)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

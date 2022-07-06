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
        # Create style used by default for all Frames
        s.configure('TFrame', background="#1E2130")
        self.lmain = tk.Label(self, borderwidth=0)
        self.lmain.grid()
        global cap
    def set_controller(self,controller):
        self.controller = controller

    def runVideoStream(self):
        ret, frame = cap.read()
        frame = cv2.resize(frame,(800,450),fx=0,fy=0, interpolation = cv2.INTER_CUBIC)
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.lmain.imgtk = imgtk
        self.lmain.configure(image=imgtk)
        self.lmain.after(1, self.runVideoStream)

    def releaseVideoStream():
        cap.release()

    def setVideoStreamDevice(device):
        cap = cv2.VideoCapture(device)
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 0)
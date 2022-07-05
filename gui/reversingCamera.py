import tkinter as tkinter

class View(tkk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.controller = None

    def set_controller(self,controller):
        self.controller = controller
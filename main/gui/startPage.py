import tkinter as tk
from tkinter import ttk

class startPage(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent)
        self.controller = None
        # Initialize style
        s = ttk.Style()
        # Create style used by default for all Frames
        s.configure('TFrame', background="#1E2130")
        #self.frame = parent
        #label = ttk.Label(self, text="This is the start page")
        self.label = tk.Label(self, text="Norvag Leasing",bg="#1E2130",fg='white',font=("Open sans", 45))
        self.label.place(relx=.5, rely=.5, anchor="c",)

    def set_controller(self,controller):
        self.controller = controller
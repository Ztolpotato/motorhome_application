from motorhome_application.gui import reversingCamera

class MotorHomeApplication(tk.Tk):
    def __init__(self):
        super().__init__()
        print("Starting...")
        self.title("MotorHome sensor and reversing camera application")
        model = Model()
        view = View(self)
        view.grid(row=0,column=0,padx=10,pady=10)
        controller = Controller(view,model)
        view.set_controller(controller)

if __name__ == '__main__':
    MotorHomeApplication()
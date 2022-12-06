
from tkinter import ACTIVE, DISABLED, Button

from canvas import TaskCanvas



#TODO: create a dict for the two buttons and organize it properly
button_auto_info = {
    "x": 70,
    "y": 500,
    "width": 150,
    "height": 50,
    "text": "Assisted Mode",
    "state": DISABLED
}

button_manual_info = {
    "x": 70,
    "y": 560,
    "width": 150,
    "height": 50,
    "text": "Manual Mode",
    "state": ACTIVE
}

button_yes_info = {
    "x": 1250,
    "y": 940,
    "width": 100,
    "height": 30,
    "text": "Yes",
    "state": ACTIVE
}

button_no_info = {
    "x": 1350,
    "y": 940,
    "width": 100,
    "height": 30,
    "text": "No",
    "state": ACTIVE
}

button_start_info = {
    "x": 1300,
    "y": 940,
    "width": 100,
    "height": 30,
    "text": "Start",
    "state": ACTIVE
}

class BaseButton():
    def __init__(self, r, info_dict, activate=True, enable = True):
        self.x = info_dict["x"]
        self.y = info_dict["y"]
        self.width = info_dict["width"]
        self.height = info_dict["height"]
        self.text = info_dict["text"]
        self.state = info_dict["state"]
        self.active = True if self.state == ACTIVE else False
        self.button = Button(r, width= self.width, height=self.height, 
            text= self.text)
        
        if enable == True: self.enable()
        elif enable == False: self.disable()
        if activate == True: self.activate()
        elif activate == False: self.deactivate()
    def add_event(self, event):
        self.button.config(command=event)
    def enable(self):
        self.button.config(state=ACTIVE)
        self.active = not self.active
    def disable(self):
        self.button.config(state=DISABLED)
        self.active = not self.active
    def deactivate(self):
        self.button.place(x = 5000, y = self.y, width=self.width, height=self.height)
    def activate(self):
        self.button.place(x = self.x, y = self.y, width=self.width, height=self.height)

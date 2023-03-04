
from tkinter import ACTIVE, DISABLED, Button

from canvas import TaskCanvas

from event import *

#TODO: create a dict for the two buttons and organize it properly
button_auto_info = {
    "x": 70,
    "y": 500,
    "width": 150,
    "height": 50,
    "text": "Assisted Mode",
    "state": DISABLED,
    "tag": 1
}

button_manual_info = {
    "x": 70,
    "y": 560,
    "width": 150,
    "height": 50,
    "text": "Manual Mode",
    "state": ACTIVE,
    "tag": 2
}

button_yes_info = {
    "x": 1250,
    "y": 940,
    "width": 100,
    "height": 30,
    "text": "Yes",
    "state": ACTIVE,
    "tag": 3
}

button_no_info = {
    "x": 1350,
    "y": 940,
    "width": 100,
    "height": 30,
    "text": "No",
    "state": ACTIVE,
    "tag": 3
}

button_start_info = {
    "x": 1300,
    "y": 940,
    "width": 100,
    "height": 30,
    "text": "Start",
    "state": ACTIVE,
    "tag": 5
    
}

button_freeze_info = {
    "x": 70,
    "y": 900,
    "width": 150,
    "height": 50,
    "text": "Freeze",
    "state": ACTIVE,
    "tag": 6
    
}

class BaseButton():
    def __init__(self, r, info_dict, activate=True, enable = True):
        self.x = info_dict["x"]
        self.y = info_dict["y"]
        self.width = info_dict["width"]
        self.height = info_dict["height"]
        self.text = info_dict["text"]
        self.state = info_dict["state"]
        self.tag = info_dict["tag"]
        self.active = True if self.state == ACTIVE else False
        self.button = Button(r, width= self.width, height=self.height, 
            text= self.text)

        
        if enable == True: self.enable()
        elif enable == False: self.disable()
        
        
        if activate == True: self.activate()
        elif activate == False: self.deactivate()

        EventManager.subscribe("button_activate", self.enable_event)
        EventManager.subscribe("freeze", self.enable_freeze)
        EventManager.subscribe("unfreeze", self.disable_freeze)
        
    def add_event(self, event):
        self.button.config(command=event)
    
    def enable_event(self, tag=0):
        if(self.tag == tag):
            self.button.config(state=ACTIVE)

    def enable(self):
        self.button.config(state=ACTIVE)

    def disable(self):
        self.button.config(state=DISABLED)

    def enable_freeze(self, tag=-1):
        if(self.tag == 6):
            self.button.config(state=ACTIVE)

    def disable_freeze(self, tag=-1):
        if(self.tag == 6):
            self.button.config(state=DISABLED)       




    def deactivate(self):
        self.button.place(x = 5000, y = self.y, width=self.width, height=self.height)
    
    def activate(self):
        self.button.place(x = self.x, y = self.y, width=self.width, height=self.height)

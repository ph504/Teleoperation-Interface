import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/model/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/control/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/view/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/utils/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/test/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/data/')



import tkinter as tk
import canvas
import event_manager


class BaseButton():
    def __init__(self, r, info_dict, activate=True, enable = True):
        self.x = info_dict["x"]
        self.y = info_dict["y"]
        self.width = info_dict["width"]
        self.height = info_dict["height"]
        self.text = info_dict["text"]
        self.state = info_dict["state"]
        self.tag = info_dict["tag"]
        self.active = True if self.state == tk.ACTIVE else False
        self.button = Button(r, width= self.width, height=self.height, 
            text= self.text)

        
        if enable == True: self.enable()
        elif enable == False: self.disable()
        
        
        if activate == True: self.activate()
        elif activate == False: self.deactivate()

        EventManager.subscribe("button_activate", self.enable_event)
        EventManager.subscribe("freeze", self.enable_freeze)
        EventManager.subscribe("unfreeze", self.disable_freeze)
        
    def add_event(self, event, arg = None):
            self.button.config(command=event)
            
        
       
    
    def enable_event(self, tag=0):
        if(self.tag == tag):
            self.button.config(state=ACTIVE)

    def enable(self):
        if self.text == "Assisted Mode" or self.text == "Manual Mode":
            self.button.config(background="#faf289", activebackground="#faf289")
        self.button.config(state=ACTIVE)

    def disable(self):
        if self.text == "Assisted Mode" or self.text == "Manual Mode":
            self.button.config(background="#d9d7bd")
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

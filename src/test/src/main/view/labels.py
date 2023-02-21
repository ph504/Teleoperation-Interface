from tkinter import *
import time
import threading



big_cmr_lbl = {
    "x": 860,
    "y": 130,
    "width": 200,
    "height": 20,
    "font": ('Helvetica', '13', 'bold')
}

small_cmr_lbl = {
    "x": 120,
    "y": 35,
    "width": 200,
    "height": 15,
    
    "font": ('Helvetica', '10', 'bold')

}
class CameraLabel():
    def __init__(self, r, label_info, text):
        self.x = label_info["x"]
        self.y = label_info["y"]
        self.width = label_info["width"]
        self.height = label_info["height"]
        self.text = text
        self.font = label_info["font"]
        
        
        self.label = Label(r, text= self.text, font=self.font)
        self.label.place(x = self.x , y = self.y, width = self.width, height = self.height)


    def switch_camera(self):
        if self.text == "Front Camera":
            self.text = "Back Camera"
            self.label.config(text = self.text)
        elif self.text == "Back Camera":
            self.text = "Front Camera"
            self.label.config(text = self.text)
            
            
    
        



        
from tkinter import *
import time
import threading
from event import EventManager
import subprocess


big_cmr_label = {
    "x": 860,
    "y": 130,
    "width": 200,
    "height": 20,
    "font": ('Helvetica', '13', 'bold')
}

small_cmr_label = {
    "x": 120,
    "y": 35,
    "width": 200,
    "height": 15,
    
    "font": ('Helvetica', '10', 'bold')

}

calibrate_label = {
    "x": 5,
    "y": 815,
    "width": 300,
    "height": 20,
    "color": "red",
    "font": ('Helvetica', '9', 'bold')
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



        EventManager.subscribe("label_camera_switch", self.switch_camera)

    def switch_camera(self, dummy = -1):
        if self.text == "Front Camera":
            self.text = "Back Camera"
            self.label.config(text = self.text)
        elif self.text == "Back Camera":
            self.text = "Front Camera"
            self.label.config(text = self.text)
            
            
    

class CalibrateLabel():
    def __init__(self, r, label_info, text):
        self.x = label_info["x"]
        self.y = label_info["y"]
        self.width = label_info["width"]
        self.height = label_info["height"]
        self.text = text
        self.font = label_info["font"]
        self.color = label_info["color"]
        
        
        self.label = Label(r, text= self.text, font=self.font, fg=self.color, anchor='s')
        self.label.place(x = self.x , y = self.y, width = self.width, height = self.height)

    def activate(self):
        subprocess.Popen("/home/pouya/catkin_ws/camera_calib.sh", shell=True)
        EventManager.post_event("calibrate_pause", -1)
        threading.Thread(target=self.calibration_label).start()
        
    def calibration_label(self):
        self.label.configure(text="calibrating ...")
        time.sleep(20)
        self.label.config(text="") 
        EventManager.post_event("calibrate_start", -1)
      
   



        
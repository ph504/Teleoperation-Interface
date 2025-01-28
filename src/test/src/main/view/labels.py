import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/model/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/control/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/view/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/utils/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/test/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/data/')

import tkinter as tk
import time
import threading
from event_manager import EventManager
import subprocess
import global_statics as gs
import global_config as gv


class CameraLabel():
    def __init__(self, r, label_info, text):
        self.x = label_info["x"]
        self.y = label_info["y"]
        self.width = label_info["width"]
        self.height = label_info["height"]
        self.text = text
        self.font = label_info["font"]
        
        
        self.label = tk.Label(r, text= self.text, font=self.font)
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
        
        
        self.label = tk.Label(r, text= self.text, font=self.font, fg=self.color, anchor='s')
        self.label.place(x = self.x , y = self.y, width = self.width, height = self.height)

    def activate(self):
        subprocess.Popen("/home/ph504/Desktop/Projects/Teleoperation-Interface/camera_calib.sh", shell=True)
        EventManager.post_event("calibrate_pause", -1)
        threading.Thread(target=self.calibration_label).start()
        
    def calibration_label(self):
        self.label.configure(text="calibrating ...")
        time.sleep(20)
        self.label.config(text="") 
        EventManager.post_event("calibrate_start", -1)
      
   



        
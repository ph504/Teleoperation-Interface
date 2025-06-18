from main.utils.path_setup import extend_path_to_root
extend_path_to_root()


import math
import textwrap
import tkinter as tk
import numpy as np
import playsound
from main.control import event_manager
from main.utils import logger
from main.data import global_config as gv
from main.data import global_statics as gs
from main.utils import repeated_timer

class BaseCanvas():
    def __init__(self, r, info_dict):
        self.x = info_dict["x"]
        self.y = info_dict["y"]
        self.width = info_dict["width"]
        self.height = info_dict["height"]
        self.active = info_dict["active"]
        self.offset = 10
        
        self.canvas = tk.Canvas(r, bg=r.cget('bg'), width=self.width+self.offset, height=self.height+self.offset)
        _x = self.x if self.active else 5000
        self.canvas.place(x = _x , y = self.y , width= self.width+self.offset, height= self.height+self.offset)

    def enable(self):
        self.active = True
        self.canvas.place(x = self.x , y = self.y , width= self.width+self.offset, height= self.height+self.offset) 

    def disable(self):
        self.active = False
        self.canvas.place(x = 5000 , y = self.y , width= self.width+self.offset, height= self.height+self.offset)

class TimerCanvas(BaseCanvas):
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.text_color = dict_info["text_color"]
        self.font = dict_info["font"]
        self.seconds = '00'
        self.minutes = '00'
        self.text = self.minutes + ":" + self.seconds
        self.countdown = None
        self.fsm = None
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.text_color, font= self.font)

    def start(self, dummy = 0):
        if self.countdown == None:
            self.countdown = repeated_timer.RepeatedTimer(1, self.plus)
        else:
            self.countdown.start()
    def stop(self, dummy = 0):
        if self.countdown != None:
            self.countdown.stop()
    # def add_fsm(self, fsm):
    #     self.fsm = fsm
    def plus(self):
        sec = self.seconds
        sec = int(sec)
        sec += 1
        
        min = self.minutes
        min = int(min)
        
        if sec == 60:
            sec = 0
            min += 1


        self.seconds = str(sec) if sec >= 10 else '0' + str(sec) 
        self.minutes = str(min) if min >= 10 else '0' + str(min)
        self.text = self.minutes + ":" + self.seconds
        event_manager.EventManager.post_event("countdown", self.text)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.text_color, font= self.font)
    

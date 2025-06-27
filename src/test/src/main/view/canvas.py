from main.utils.path_setup import extend_path_to_root
extend_path_to_root()


import math
import textwrap
import tkinter as tk
import numpy as np
import time
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
        self.pause_time = 0
        self.start_time = 0
        self.elapsed_time_before_pause = 0
        self.running = False
        # self.countdown = None
        # self.stopwatch = threading.Event()
        # self.stopwatch.set()
        # self.fsm = None
        self.canvas.create_text(
            self.width/2, 
            self.height/2, 
            text= self.text, 
            fill= self.text_color, 
            font= self.font
        )
        self.update_loop()

    def start(self, dummy = 0):
        if not self.running:
            self.start_time = time.time()
            # self.elapsed_before_pause = 0
            self.running = True
        # if self.countdown == None:
        #     self.countdown = repeated_timer.RepeatedTimer(1, self.plus)
        # else:
        #     self.countdown.start()

    def pause(self, dummy=0):
        if self.running:
            self.pause_time = time.time()
            self.elapsed_time_before_pause += self.pause_time - self.start_time
            self.running = False

    # def resume(self, dummy=0):
    #     if not self.running:
    #         self.start_time = time.time()
    #         self.running = True

    def reset(self, dummy=0):
        self.running = False
        self.start_time = None
        self.pause_time = None
        self.elapsed_time_before_pause = 0
        self.text = "00:00"
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width / 2,
            self.height / 2,
            text=self.text,
            fill=self.text_color,
            font=self.font
        )

    # def stop(self, dummy = 0):
    #     if self.countdown != None:
    #         self.countdown.stop()
    # def add_fsm(self, fsm):
    #     self.fsm = fsm
    # def plus(self):
    #     sec = self.seconds
    #     sec = int(sec)
    #     sec += 1
        
    #     min = self.minutes
    #     min = int(min)
        
    #     if sec == 60:
    #         sec = 0
    #         min += 1


    #     self.seconds = str(sec) if sec >= 10 else '0' + str(sec) 
    #     self.minutes = str(min) if min >= 10 else '0' + str(min)
    #     self.text = self.minutes + ":" + self.seconds
    #     # event_manager.EventManager.post_event("countdown", self.text)
    #     self.canvas.delete('all')
    #     self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.text_color, font= self.font)
    
    def update_loop(self):
        if self.running and self.start_time is not None:
                elapsed = time.time() - self.start_time + self.elapsed_before_pause
                mins = int(elapsed // 60)
                secs = int(elapsed % 60)
                formatted = f"{mins:02d}:{secs:02d}"
                self.canvas.delete("all")
                self.canvas.create_text(
                    self.width / 2,
                    self.height / 2,
                    text=self.text,
                    fill=self.text_color,
                    font=self.font
                )
                logger.Logger.set_elapsed_time(formatted)
                # event_manager.EventManager.post_event("countdown", formatted)

        self.canvas.after(1000, self.update_loop)
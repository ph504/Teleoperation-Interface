from event import *
from logger import Logger
import global_variables
from tkinter import * 
import random
class UserAI():
    def __init__(self, root) -> None:
        self.root = root
        self.counter = 0
        self.mistake = 0
        
        self.is_fast = False
        self.waiting_to_hit = None

        self.bar_hitter_tag = None
        EventManager.subscribe("red_init_mode", self.mode_switchter)
        EventManager.subscribe("toggle_barmode", self.toggle_fast)


        self.counter_modecheck()




    def counter_modecheck(self):
        if global_variables.danger_mode:
            self.counter += 1   
            if self.counter >= 10 and self.mistake <= 3:
                if not self.waiting_to_hit:
                    self.bar_hitter_tag = random.randint(1,3)
                    self.hitter()
                    self.waiting_to_hit = True
                    self.counter = 0 
            elif self.counter >= 10 and self.mistake > 3:
                EventManager.post_event("bar_slow_mode", 2)
                self.waiting_to_hit = False
        else:
            
            self.mistake = 0
            self.counter = 0
            self.waiting_to_hit = False
        Tk.after(self.root, 1000, self.counter_modecheck)

        
    def hitter(self):
        
        if self.mistake == 0:
            if global_variables.in_inspection:
                EventManager.post_event("bar_ultra_mode", self.bar_hitter_tag)
                return
        elif self.mistake == 1:
            if not global_variables.in_inspection:
                EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                return
        elif self.mistake == 2:
            if global_variables.in_inspection:
                EventManager.post_event("bar_ultra_mode", self.bar_hitter_tag)
                return

        Tk.after(self.root, 100, self.hitter)

    def mode_switchter(self, dummy = -1):
        if global_variables.danger_mode and not global_variables.jackalai_active:
            self.counter = 0
            self.mistake += 1
            if self.mistake <= 3:
                if self.waiting_to_hit:
                    EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                    self.waiting_to_hit = False
            if self.mistake > 3:
                EventManager.post_event("bar_slow_mode", self.bar_hitter_tag
                                        )
                self.waiting_to_hit = False
    
    
    
    def toggle_fast(self):
        if self.waiting_to_hit == False:
            self.waiting_to_hit = True
        else:
            self.waiting_to_hit = False

import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/')

from main.control import event_manager
from main.utils import logger
from main.data import global_config as gv
from tkinter import Tk
import random
import playsound


class JackalAI():
    
    gv.jackalai_active = False

    def __init__(self, root):
        self.root = root
        self.right_count = 0
        self.wrong_count = 0
        self.count = 0
        self.first_mistake = False
        self.second_mistake = False
        self.first_time = False
        self.second_time = False
        self.step_error_count = 0
        self.step_error_max = 3
        
        self.correct_logging = 0
        # EventManager.subscribe("yellow_mode", self.press_yellow) # type: ignore
        # EventManager.subscribe("red_init_mode", self.press_red_init) # type: ignore
        # EventManager.subscribe("step_error_danger", self.press_red) # type: ignore
        self.incorrect_logging = 0
        #EventManager.subscribe("red_mode", self.press_red) #TODO:What?
        self.bar_hitter_tag = None
        self.bar_hit_count = 0
        self.waiting_to_hit = None
        # EventManager.subscribe("red_init_mode", self.mode_switchter) # type: ignore

        self.max_mistake = 5
        self.max_barhitcount = 6
        # EventManager.subscribe("assisted_second", self.second_round) # type: ignore

        self.c_maxcount = 15

        self.COLOR_TASK_TRANSITION_YELLOW = 2
        self.COLOR_TASK_TRANSITION_ORANGE = 5
        #TODO: bar hit count should be flexible
        self.counter_modecheck()     

    def second_round(self, dummy = -1):
        self.mistake = 0
        self.bar_hit_count = 0 

        self.max_mistake = 0
        self.max_barhitcount = 1

        self.counter = 0

    # def press_yellow(self, bar: BarCanvas):    
        
    #     if gv.jackalai_active:
           
    #         if self.bar_hit_count <= self.max_barhitcount and bar.bar_tag == self.bar_hitter_tag:

    #             self.count -= 1
    #             self.bar_hit_count += 1
    #             return
    #         else:
  
    #             self.count += 1
    #             self.correct_logging += 1
    #             Logger.log("ai_correctlogging", self.correct_logging) # type: ignore
                
    #             bar.jackal_reset("yellow")
                
    # def press_red_init(self, bar: BarCanvas):   
    #     if gv.jackalai_active:
                
    #             if self.first_time and self.bar_hit_count == self.COLOR_TASK_TRANSITION_YELLOW:
    #                 EventManager.post_event("color_trans", -1) 
                


    #             EventManager.post_event("mistake", -1)
    #             self.count += 1
    #             self.incorrect_logging  += 1
    #             Logger.log("ai_incorrectlogging", self.incorrect_logging)
                
    #             bar.jackal_reset("red_init")                                         
    
    # def press_red(self, bar: BarCanvas):
        
    #     if gv.jackalai_active and gv.danger_mode: 

    #         self.press_red_init(bar)
    #         self.mode_switchter()

    def enable(self):     
        if not self.first_time and not self.second_time:
            self.first_time = True
        elif self.first_time and not self.second_time:
            self.first_time = False
            self.second_time = True
        
        self.count = 0
        
        gv.jackalai_active = True

    def disable(self):
        gv.jackalai_active = False

    def hitter(self):
        if gv.jackalai_active:
            if self.mistake == 0:
                if not gv.in_inspection:
                    EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                    self.c_maxcount = 10
                    return
            elif self.mistake == 1:
                if not gv.in_inspection:
                    EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                    return
            elif self.mistake == 2:
                if not gv.in_inspection:
                    EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                    return
            elif self.mistake == 3:
                if not gv.in_inspection:
                    EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                    return
            elif self.mistake == 4:
                if not gv.in_inspection:
                    EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                    return
            elif self.mistake == 5:
                if not gv.in_inspection:
                    EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                    return
        else:
            return
        

        Tk.after(self.root, 100, self.hitter)

    def mode_switchter(self, dummy = -1):
        if gv.danger_mode and gv.jackalai_active:
            self.counter = 0
            self.mistake += 1
            if self.mistake <= self.max_mistake:
                if self.waiting_to_hit:
                    EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                    self.waiting_to_hit = False
                    self.bar_hitter_tag = -1
            elif self.mistake > self.max_mistake:
                EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                self.waiting_to_hit = False
                self.bar_hitter_tag = -1
    
    def counter_modecheck(self):
        
        if gv.danger_mode and gv.jackalai_active:
            self.counter += 1   
            if self.counter >= self.c_maxcount and self.mistake <= self.max_mistake:
                if not self.waiting_to_hit:
                    self.bar_hitter_tag = random.randint(1,3)
                    self.hitter()
                    self.waiting_to_hit = True
                    self.counter = 0 
            elif self.counter >= self.c_maxcount and self.mistake > self.max_mistake:
                EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                self.waiting_to_hit = False
                self.bar_hitter_tag = -1
        else:
            self.mistake = 0
            self.counter = 0
            self.waiting_to_hit = False
            self.bar_hitter_tag = -1
        
        
        Tk.after(self.root, 1000, self.counter_modecheck)
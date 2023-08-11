from bar_canvas import BarCanvas
from event import *
from logger import Logger
import global_variables
import random
from tkinter import Tk
import playsound


class JackalAI():
    
    global_variables.jackalai_active = False

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
        EventManager.subscribe("yellow_mode", self.press_yellow)
        EventManager.subscribe("red_init_mode", self.press_red_init)
        EventManager.subscribe("step_error_danger", self.press_red)
        self.incorrect_logging = 0
        #EventManager.subscribe("red_mode", self.press_red) #TODO:What?
        self.bar_hitter_tag = None
        self.bar_hit_count = 0
        self.waiting_to_hit = None
        EventManager.subscribe("red_init_mode", self.mode_switchter)

        self.max_mistake = 3
        self.max_barhitcount = 4
        EventManager.subscribe("assisted_second", self.second_round)

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

    def press_yellow(self, bar: BarCanvas):    
        
        if global_variables.jackalai_active:
           
            if self.bar_hit_count <= self.max_barhitcount and bar.bar_tag == self.bar_hitter_tag:

                self.count -= 1
                self.bar_hit_count += 1
                return
            else:
  
                self.count += 1
                self.correct_logging += 1
                Logger.log("ai_correctlogging", self.correct_logging)
                playsound.playsound("/home/pouya/catkin_ws/src/test/src/sounds/beep.wav", block=False) 
                bar.reset_button()
  
    def press_red_init(self, bar: BarCanvas):   
        if global_variables.jackalai_active:
                
                if self.first_time and self.bar_hit_count == self.COLOR_TASK_TRANSITION_YELLOW:
                    EventManager.post_event("color_trans", -1) 
                


                EventManager.post_event("mistake", -1)
                self.count += 1
                self.incorrect_logging  += 1
                Logger.log("ai_incorrectlogging", self.incorrect_logging)
                bar.reset_button(False)                                          
    
    def press_red(self, bar: BarCanvas):
        
        if global_variables.jackalai_active and global_variables.danger_mode: 

            self.press_red_init(bar)
            self.mode_switchter()
            playsound.playsound("/home/pouya/catkin_ws/src/test/src/sounds/error.wav", block=False)

    def enable(self):     
        if not self.first_time and not self.second_time:
            self.first_time = True
        elif self.first_time and not self.second_time:
            self.first_time = False
            self.second_time = True
        
        self.count = 0
        
        global_variables.jackalai_active = True

    def disable(self):
        global_variables.jackalai_active = False

    def hitter(self):
        
        if self.mistake == 0:
            if not global_variables.in_inspection:
                EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                self.c_maxcount = 10
                return
        elif self.mistake == 1:
            if not global_variables.in_inspection:
                EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                return
        elif self.mistake == 2:
            if not global_variables.in_inspection:
                EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                return
        elif self.mistake == 3:
            if not global_variables.in_inspection:
                EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                return
        

        Tk.after(self.root, 100, self.hitter)

    def mode_switchter(self, dummy = -1):
        if global_variables.danger_mode and global_variables.jackalai_active:
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
        
        if global_variables.danger_mode and global_variables.jackalai_active:
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
        
        
        Tk.after(self.root, 1000, self.counter_modecheck)
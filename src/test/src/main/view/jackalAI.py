from canvas import BarCanvas
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
        self.to_miss = global_variables.tuto_miss
    

        #TODO: bar hit count should be flexible
        self.counter_modecheck()     

    def press_yellow(self, bar: BarCanvas):    
        
        if global_variables.jackalai_active:
            print(f"1 -- bar {bar.bar_tag} is in yellow state")
            if self.bar_hit_count <= 3 and bar.bar_tag == self.bar_hitter_tag:
                print(f"2 -- bar {bar.bar_tag} is the bar to hit ({self.bar_hitter_tag}),  so it should be error!")
                self.count -= 1
                return
            else:
                print(f"4 -- jackal succesfuly handles bar {bar.bar_tag}")
                self.count += 1
                self.correct_logging += 1
                Logger.log("ai_correctlogging", self.correct_logging)
                bar.reset_button()
  
    def press_red_init(self, bar: BarCanvas):
        
        if global_variables.jackalai_active:
                
                if self.first_time and self.bar_hit_count == 2:
                    EventManager.post_event("color_trans", -1) 
                
                print(f"5 --- time to miss this time! whether because of miss or the hit!")
                EventManager.post_event("mistake", -1)
                self.count += 1
                self.incorrect_logging  += 1
                Logger.log("ai_incorrectlogging", self.incorrect_logging)
                bar.reset_button()                                          
    
    def press_red(self, bar: BarCanvas):
        
        if global_variables.jackalai_active: 
            print("6 --- why it should come here?")
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
        self.bar_hit_count += 1
        
        if self.mistake == 0:
            if not global_variables.in_inspection:
                EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
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
        print(f"7 --- It was in fast mode but has to go slow, switching mode")
        if global_variables.danger_mode and global_variables.jackalai_active:
            self.counter = 0
            self.mistake += 1
            if self.mistake <= 3:
                if self.waiting_to_hit:
                    EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                    self.waiting_to_hit = False
                    self.bar_hitter_tag = -1
            if self.mistake > 3:
                EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                self.waiting_to_hit = False
                self.bar_hitter_tag = -1
    
    def counter_modecheck(self):
        if global_variables.danger_mode and global_variables.jackalai_active:
            self.counter += 1   
            if self.counter >= 10 and self.mistake <= 3:
                if not self.waiting_to_hit:
                    self.bar_hitter_tag = random.randint(1,3)
                    self.hitter()
                    self.waiting_to_hit = True
                    self.counter = 0 
            elif self.counter >= 10 and self.mistake > 3:
                EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                self.waiting_to_hit = False
                self.bar_hitter_tag = -1
        else:
            self.mistake = 0
            self.counter = 0
            self.waiting_to_hit = False
        
        
        Tk.after(self.root, 1000, self.counter_modecheck)
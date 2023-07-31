from event import *
from logger import Logger
import global_variables
from tkinter import * 
import random
from canvas import BarCanvas
from collections import deque

class UserAI():
    def __init__(self, root) -> None:
        self.root = root
        self.counter = 0
        self.mistake = 0
        
        self.is_fast = False
        self.waiting_to_hit = None

        self.bar_hitter_tag = None
        EventManager.subscribe("user_reset", self.bar_hit_slow)
        EventManager.subscribe("red_init_mode", self.mode_switchter)
        EventManager.subscribe("yellow_mode", self.normal_counterback)

        self.MAX_COUNT_TUTORIAL = 4 #number of mistakes that has to happen in tutorial for the user
        self.MAX_COUNT_EXPERIMENT = 3 #number of mistakes that has to happen in experiment for the user



        self.m_max_count = None #containter for max num of mistakes base on condition

        if global_variables.tutorial_mode:
            self.m_max_count = self.MAX_COUNT_TUTORIAL
        else:
            self.m_max_count = self.MAX_COUNT_EXPERIMENT


        self.c_max_count = 10 #number of seconds that has to pass so a mistake happens

        
        f = "bar_fast_mode"
        u = "bar_ultra_mode"
        
        self.tutorial_q = deque(
            [ u , f , u , f ]
            )
        
        self.experiment_q = deque(
            [ u , f , u ]
        )
       
        self.q = None
        
        if global_variables.tutorial_mode:
            self.q = self.tutorial_q
        else:
            self.q = self.experiment_q

        self.counter_modecheck()

    def normal_counterback(self, bar: BarCanvas):

        if global_variables.danger_mode and not global_variables.jackalai_active and self.mistake >= self.m_max_count:
            EventManager.post_event("move_bar_backward", bar)

    def counter_modecheck(self):
        if global_variables.danger_mode and not global_variables.jackalai_active:
            self.counter += 1   
            if self.counter >= self.c_max_count and self.mistake <= self.m_max_count:
                if not self.waiting_to_hit:
                    self.bar_hitter_tag = random.randint(1,3)
                    self.hitter()
                    self.waiting_to_hit = True
                    self.counter = 0 
            elif self.counter >= self.c_max_count and self.mistake > self.m_max_count:
                EventManager.post_event("bar_slow_mode", 2)
                self.waiting_to_hit = False
        else:
            
            self.mistake = 0
            self.counter = 0
            self.waiting_to_hit = False
        Tk.after(self.root, 1000, self.counter_modecheck)
     
    
    def hitter_test(self):
        print(len(self.q))
        if len(self.q) != 0 and global_variables.in_inspection:
            print("*** -- here")
            EventManager.post_event(self.q.popleft(), self.bar_hitter_tag)
    
    
    
    def hitter(self):
        if global_variables.tutorial_mode:
            
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
            elif self.mistake == 3:
                if not global_variables.in_inspection:
                    EventManager.post_event("bar_fast_mode", self.bar_hitter_tag)
                    
                    return
        
        else:    
            
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
            
            if self.mistake == 2: EventManager.post_event("color_trans", -1) 
            
            print("human mistake " + str(self.mistake))
            
            if self.mistake <= self.m_max_count:

                if self.waiting_to_hit:
                    EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                    self.bar_hitter_tag = -1
                    self.waiting_to_hit = False

            if self.mistake > self.m_max_count:
                EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                self.bar_hitter_tag = -1
                self.waiting_to_hit = False

    
    def bar_hit_slow(self, bar:BarCanvas):
        if global_variables.danger_mode and not global_variables.jackalai_active:
            if bar.bar_tag == self.bar_hitter_tag:
                print("the success press -- goes to slow")
                EventManager.post_event("bar_slow_mode", self.bar_hitter_tag)
                self.bar_hitter_tag = -1
                #self.mistake += 1
                self.waiting_to_hit = False
                #print("human mistake " + str(self.mistake))

    def toggle_fast(self):
        if self.waiting_to_hit == False:
            self.waiting_to_hit = True
        else:
            self.waiting_to_hit = False

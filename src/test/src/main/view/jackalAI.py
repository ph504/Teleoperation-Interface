from canvas import BarCanvas
from event import *
from logger import Logger
import global_variables


class JackalAI():
    
    global_variables.jackalai_active = True

    def __init__(self):
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
    
    def press_yellow(self, bar: BarCanvas):  
        
        if global_variables.jackalai_active:
            if self.first_time:
                if self.count == 2 or self.count == 5 or self.count == 8:
                    return
            elif self.second_time:
                if self.count == 3 or self.count == 6:
                    return
            
            self.count += 1
            self.correct_logging += 1
            Logger.log("ai_correctlogging", self.correct_logging)
            bar.reset_button()
  
    def press_red_init(self, bar: BarCanvas):
        if global_variables.jackalai_active:
                print("count for jackal AI: " + str(self.count))
                if self.first_time and self.count == 5:
                    EventManager.post_event("color_trans", -1) 
                self.count += 1
                EventManager.post_event("mistake", -1)
                
                self.incorrect_logging  += 1
                Logger.log("ai_incorrectlogging", self.incorrect_logging)
                bar.reset_button()                                          
    
    def press_red(self, bar: BarCanvas):
        
        if global_variables.jackalai_active: 
            print("here!")   
            self.step_error_count += 1
            if self.step_error_count == 1:
                bar.reset_button()
                self.step_error_count = 0

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
        
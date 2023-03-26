from canvas import BarCanvas
from event import *
from logger import Logger
class JackalAI():
    
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
        self.active = False
        self.correct_logging = 0
        EventManager.subscribe("yellow_mode", self.press_yellow)
        EventManager.subscribe("red_init_mode", self.press_red_init)
        self.incorrect_logging = 0
        #EventManager.subscribe("red_mode", self.press_red) #TODO:What?
    def press_yellow(self, bar: BarCanvas):  
        
        if self.active:
            if self.count == 2 or self.count == 5 or self.count == 8:
                return
            else:
                self.count += 1
                self.correct_logging += 1
                Logger.log("ai_correctlogging", self.correct_logging)
                bar.reset_button()
  
    def press_red_init(self, bar: BarCanvas):
        if self.active:
                print("count for jackal AI: " + str(self.count))
                if self.count == 5:
                    EventManager.post_event("color_trans", -1) 
                self.count += 1
                EventManager.post_event("mistake", -1)
                
                self.incorrect_logging  += 1
                Logger.log("ai_incorrectlogging", self.incorrect_logging)
                bar.reset_button()
                
                
            
            
    def press_red(self, bar: BarCanvas):
        if self.active:    
            self.step_error_count += 1
            if self.step_error_count == self.step_error_max:
                bar.reset_button()
                self.step_error_count = 0

    def enable(self):
        self.active = True

    def disable(self):
        self.active = False
        self.count = 15
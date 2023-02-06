from canvas import BarCanvas
from event import *

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

        subscribe("yellow_mode", self.press_yellow)
        subscribe("red_init_mode", self.press_red_init)

        #subscribe("red_mode", self.press_red) #TODO:What?
    def press_yellow(self, bar: BarCanvas):  
        if self.count == 5 or self.count == 10:
            return
        else:
            self.count += 1
            bar.reset_button()
  
    def press_red_init(self, bar: BarCanvas):
        if self.count == 5 or self.count == 10:
            self.count += 1
            post_event("mistake", -1)
            bar.reset_button()
            
            
    def press_red(self, bar: BarCanvas):
        self.step_error_count += 1
        if self.step_error_count == self.step_error_max:
            bar.reset_button()
            self.step_error_count = 0

        
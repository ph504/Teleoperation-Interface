import math
from textwrap import fill
from tkinter import *
import numpy
import threading
import random
from playsound import playsound
from event import *
import string
from logger import Logger
import global_variables
#------Canvas Position ---- #
big_canvas_info = {
    "x": 1500,
    "y": 600,
    "width": 150,
    "height": 150,
    "endup_angle": numpy.deg2rad(-90),
    "endleft_angle": numpy.deg2rad(-240),
    "endright_angle": numpy.deg2rad(60),
    "outline_color": "SpringGreen3",
    "outline_width": 5,
    "color": "green",
    "active": True
}
small_canvas_info = {
    "x": 430,
    "y": 250,
    "width": 50,
    "height": 50,
    "endup_angle": numpy.deg2rad(-90),
    "endleft_angle": numpy.deg2rad(-240),
    "endright_angle": numpy.deg2rad(60),
    "outline_color": "SpringGreen3",
    "outline_width": 2,
    "color": "green",
    "active": False


}
bar_canvas_info_main = {
    "x": 560,
    "y": 70,
    "width": 800,
    "height": 20,
    "bar_defaultpercent": 50/100,
    "line_thresholdpercent": 80/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "blue",
    "line_color": "red",
    "line_width": 2,
    "move_interval": 0.7,
    "progress_step": 0.5,
    "active": True

}
bar_canvas_info1 = {
    "x": 560,
    "y": 30,
    "width": 800,
    "height": 20,
    "bar_defaultpercent": 20/100,
    "line_thresholdpercent": 80/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "green",
    "line_color": "red",
    "line_width": 2,
    "move_interval": 0.75,
    "progress_step": 5,
    "active": False

}
bar_canvas_info2 = {
    "x": 560,
    "y": 60,
    "width": 800,
    "height": 20,
    "bar_defaultpercent": 40/100,
    "line_thresholdpercent": 80/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "green",
    "line_color": "red",
    "line_width": 2,
    "move_interval": 0.25,
    "progress_step": 1,
    "active": False

}
bar_canvas_info3 = {
    "x": 560,
    "y": 90,
    "width": 800,
    "height": 20,
    "bar_defaultpercent": 25/100,
    "line_thresholdpercent": 80/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "green",
    "line_color": "red",
    "line_width": 2,
    "move_interval": 0.5,
    "progress_step": 3,
    "active": False

}
timer_canvas_info = {
    "x": 1650,
    "y": 75,
    "width": 200,
    "height": 50,
    "color": "red",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}
timer_lbl_info = {
    "x": 1725,
    "y": 60,
    "width": 50,
    "height": 17,
    "color": "red",
    "font": ('Helvetica', '12', 'bold'),
}
task_canvas_info = {
    "x": 1600,
    "y": 75,
    "width": 100,
    "height": 50,
    "color": "green",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}
task_lbl_info = {
    "x": 1625,
    "y": 60,
    "width": 50,
    "height": 17,
    "color": "green",
    "font": ('Helvetica', '12', 'bold'),

}
score_canvas_info = {
    "x": 1450,
    "y": 75,
    "width": 150,
    "height": 50,
    "color": "blue",
    "font": ('Helvetica', '24', 'bold'),
    "active": False
}
score_lbl_info = {
    "x": 1500,
    "y": 60,
    "width": 50,
    "height": 17,
    "color": "blue",
    "font": ('Helvetica', '12', 'bold'),

}
score_events = {
    "step_error": 5,
    "step_error_danger": 25,
    
    "threshold_cross": 25,
    "threshold_cross_danger": 50,
    
    "collision_hit": 50,
    
    "wrong_entry": 25,
    "duplicate_entry": 10,

    "task_count": 100
}
circle_canvas_info = {
    "x": 1550,
    "y": 290,
    "width": 802,
    "height": 602,
    "colors": {"light_green": '#03fc0f', "yellow": '#ecfc03', "orange": '#f75a05', "red": "#fc0303"},
    "active": True
}



class RepeatedTimer(object):
    def __init__(self, interval, function, *args, **kwargs):
        self._timer     = None
        self.interval   = interval
        self.function   = function
        self.args       = args
        self.kwargs     = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args, **self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

        
    def change_args(self, *args):
        self.args = args

class BaseCanvas():
    def __init__(self, r, info_dict):
        self.x = info_dict["x"]
        self.y = info_dict["y"]
        self.width = info_dict["width"]
        self.height = info_dict["height"]
        self.active = info_dict["active"]
        self.offset = 10
        
        self.canvas = Canvas(r, bg=r.cget('bg'), width=self.width+self.offset, height=self.height+self.offset)
        _x = self.x if self.active else 5000
        self.canvas.place(x = _x , y = self.y , width= self.width+self.offset, height= self.height+self.offset)

    def enable(self):
        self.active = True
        self.canvas.place(x = self.x , y = self.y , width= self.width+self.offset, height= self.height+self.offset) 

    def disable(self):
        self.active = False
        self.canvas.place(x = 5000 , y = self.y , width= self.width+self.offset, height= self.height+self.offset)

class CursorCanvas(BaseCanvas):
    def __init__(self, r, info_dict):
        super().__init__(r,info_dict)
        self.a_up = info_dict["endup_angle"]
        self.a_left = info_dict["endleft_angle"]
        self.a_right = info_dict["endright_angle"]
        self.outline_color = info_dict["outline_color"]
        self.color = info_dict["color"]
        self.outline_width = info_dict["outline_width"]

        self.angle_diff = 1

        cursor_endpoints = self.create_arrowpoints()
        self.canvas.create_polygon(cursor_endpoints, outline=self.outline_color, fill=self.color, width=self.outline_width)
    def create_arrowpoints(self):
    
        center_x = self.width/2
        center_y = self.height/2
    
        length = self.width /2


        endup_x = center_x + length * math.cos(self.a_up)
        endup_y = center_y + length * math.sin(self.a_up)

        endleft_x = center_x + length * math.cos(self.a_left)
        endleft_y = center_y + length * math.sin(self.a_left)

        endright_x = center_x + length * math.cos(self.a_right)
        endright_y = center_y + length * math.sin(self.a_right)

        points = [endup_x, endup_y, endleft_x, endleft_y, center_x, center_x,  endright_x, endright_y]
    
    
        return points
    def rotate(self, string):

        if string == "right":
            self.a_up += numpy.deg2rad(self.angle_diff)
            self.a_left += numpy.deg2rad(self.angle_diff)
            self.a_right += numpy.deg2rad(self.angle_diff)
        elif string == "left":
            self.a_up -= numpy.deg2rad(self.angle_diff)
            self.a_left -= numpy.deg2rad(self.angle_diff)
            self.a_right -= numpy.deg2rad(self.angle_diff)
        
        new_cursor_endpoints = self.create_arrowpoints()
        self.canvas.delete('all')
        self.canvas.create_polygon(new_cursor_endpoints, outline=self.outline_color, fill=self.color, width=self.outline_width)

class BarCanvas(BaseCanvas): 
    danger_mode = None
    danger_count = 0
    manual_mode = None

    def __init__(self, r, info_dict, danger):
        super().__init__(r,info_dict)
        self.bar_percent = info_dict["bar_defaultpercent"]
        self.bar_defaultpercent = self.bar_percent
        self.tag_bar = "bar"
        self.tag_line = "line"
        self.outline_color = info_dict["outline_color"]
        self.bar_color = info_dict["color"]
        self.line_color = info_dict["line_color"]
        self.outline_width = info_dict["outline_width"]
        self.line_width = info_dict["line_width"]
        self.line_thresholdpercent = info_dict["line_thresholdpercent"]
        self.repeat_moving = None
        self.active = info_dict["active"]
        self.secondary_task = None
        self.move_interval= info_dict["move_interval"]
        self.progress_step = info_dict["progress_step"]
        self.canvas.create_rectangle(2,2, self.width, self.height, fill=r.cget('bg'), outline=self.outline_color, width=self.outline_width)
        self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill=self.bar_color, tags=self.tag_bar)
        self.canvas.create_line(self.width*self.line_thresholdpercent,0,self.width*self.line_thresholdpercent,self.height, fill=self.line_color, width=self.outline_width, tags=self.tag_line)
        self.passed = False
        self.is_danger = danger
        self.red_mode = False
        
        self.threshold_pass_count_normal = 0
        self.threshold_pass_count_danger = 0
        self.step_pass_count_normal = 0
        self.step_pass_count_danger = 0
        EventManager.subscribe("count_manual_trans_deactive", self.manual_deactive)
        EventManager.subscribe("count_manual_trans_active", self.manual_active)

    def start(self):
        #self.secondary_task = RepeatedTimer(random.randint(1,10), self.random_movement)
        self.secondary_task = RepeatedTimer(3, self.random_movement)
    
    def move_bar(self,string):   
        #just to prevent danger bars being active while normal is active (and vice versa) 
        if (self.is_danger and BarCanvas.danger_mode) or (not self.is_danger and not BarCanvas.danger_mode):
            
            self.canvas.delete(self.tag_bar,self.tag_line)
            if string == "left" and self.bar_percent > 0: self.bar_percent -= self.progress_step / 100
            elif string == "right" and self.bar_percent < 100: self.bar_percent += self.progress_step / 100
            
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill=self.bar_color, tags=self.tag_bar)
            self.canvas.create_line(self.width*self.line_thresholdpercent,0,self.width * self.line_thresholdpercent,self.height, fill=self.line_color, width=self.line_width, tags=self.tag_line)

            self.colorchange_check()
            self.canvas.tag_raise(self.tag_line,self.tag_bar)
    
    def colorchange_check(self):     
        #check to see the time the bar has passed the threshold 
        if not self.passed and self.bar_percent > self.line_thresholdpercent:
            self.passed = True
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill="yellow", tags=self.tag_bar)
            self.canvas.create_line(self.width * self.line_thresholdpercent, 0, self.width * self.line_thresholdpercent, self.height, fill=self.line_color, width=self.line_width, tags=self.tag_line)
            if self.is_danger: EventManager.post_event("yellow_mode", self) 
            
        #if the bar moves backward it may get less than the threshold 
        if self.passed and self.bar_percent < self.line_thresholdpercent:
            self.passed = False
            return
        
        # check to see if the user ignored and the bar is just keep going 
        elif self.passed and self.bar_percent > self.line_thresholdpercent + self.progress_step/100:
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill="red", tags=self.tag_bar)
            self.canvas.create_line(self.width * self.line_thresholdpercent, 0, self.width * self.line_thresholdpercent, self.height, fill="blue", width=self.line_width, tags=self.tag_line)
            
            if self.red_mode:
                if self.is_danger:
                    EventManager.post_event("step_error_danger", self)
                    self.step_pass_count_danger += 1
                    print(self.step_pass_count_danger)
                    Logger.log("stppsscount_dngr", self.step_pass_count_danger)
                else: 
                    self.step_pass_count_normal += 1
                    Logger.log("stppsscount_nrml", self.step_pass_count_normal)
                    EventManager.post_event("step_error") 
                
                EventManager.post_event("red_mode", self) #LOG?
               
            else:
                if self.is_danger:
                    self.threshold_pass_count_danger +=1
                    Logger.log("thrshldpsscntttl_dngr", self.threshold_pass_count_danger)
                    EventManager.post_event("threshold_cross_danger") 
                else:
                    EventManager.post_event("threshold_cross") 
                    self.threshold_pass_count_normal +=1
                    Logger.log("thrshldpsscntdngrttl_nrml", self.threshold_pass_count_normal)
                
                if BarCanvas.danger_mode: EventManager.post_event("red_init_mode", self)
                
                self.red_mode = True
                
                if BarCanvas.danger_mode and BarCanvas.manual_mode:
                    BarCanvas.danger_count += 1
                    print("danger_count: " + str(BarCanvas.danger_count))
                    if BarCanvas.danger_count == 3:
                        EventManager.post_event("color_trans", -1)


                playsound("/home/pouya/catkin_ws/src/test/src/sounds/error.wav", block=False)
                 
    def reset_button(self):
        if self.passed == False:
            EventManager.post_event("error_push")
            return
        else:
            self.passed = False
            if not global_variables.jackalai_active or not self.red_mode:
                playsound("/home/pouya/catkin_ws/src/test/src/sounds/beep.wav") 
            
            self.red_mode = False
            
            if not self.is_danger:
                self.bar_percent = self.bar_defaultpercent
            else:
                #self.bar_percent = random.randint(20, self.line_thresholdpercent * 100) / 100
                self.bar_percent = 30/ 100
            
            self.canvas.delete(self.tag_bar,self.tag_line)
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill=self.bar_color, tags=self.tag_bar)
            self.canvas.create_line(self.width*self.line_thresholdpercent,0,self.width*self.line_thresholdpercent,self.height, fill=self.line_color, width=self.line_width, tags=self.tag_line)

    def reset(self):
        self.passed = False
        self.bar_percent = self.bar_defaultpercent
        self.canvas.delete(self.tag_bar,self.tag_line)
        self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill=self.bar_color, tags=self.tag_bar)
        self.canvas.create_line(self.width*self.line_thresholdpercent,0,self.width*self.line_thresholdpercent,self.height, fill=self.line_color, width=self.line_width, tags=self.tag_line)
    
    def manual_active(dummy1, dummy2):
        BarCanvas.manual_mode = True
        BarCanvas.danger_count = 0
        print("manual mode is activated")
    
    def manual_deactive(dummy1, dummy2):
        BarCanvas.manual_mode = False       

    def move_bar_repeat(self, string, interval):
        if global_variables.tutorial_mode:
            if global_variables.bar_controller and self.repeat_moving is None:
                return 
            elif global_variables.bar_controller and self.repeat_moving is not None:
                self.repeat_moving.stop()
            elif not global_variables.bar_controller:
                if self.repeat_moving is not None:
                    self.repeat_moving.stop()
                    self.repeat_moving.change_args(string)
                    self.repeat_moving.start()
                else:
                    self.repeat_moving = RepeatedTimer(interval, self.move_bar, string)  
        else:
            if self.repeat_moving is not None:
                self.repeat_moving.stop()
                self.repeat_moving.change_args(string)
                self.repeat_moving.start()
            else:
                self.repeat_moving = RepeatedTimer(interval, self.move_bar, string)  
    
    
    def random_movement(self):
        #r = random.randint(0,5)
        #if r > 4:
        #    self.move_bar_repeat("left", self.move_interval)
        #else:
            self.move_bar_repeat("right", self.move_interval)

class TimerCanvas(BaseCanvas):
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        self.seconds = '00'
        self.minutes = '00'
        self.text = self.minutes + ":" + self.seconds
        self.countdown = None
        self.fsm = None
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)


        EventManager.subscribe("calibrate_pause", self.stop)
        EventManager.subscribe("calibrate_start", self.start)

    def start(self, dummy = 0):
        if self.countdown == None:
            self.countdown = RepeatedTimer(1, self.plus)
        else:
            self.countdown.start()
    def stop(self, dummy = 0):
        self.countdown.stop()
    def add_fsm(self, fsm):
        self.fsm = fsm
    def plus(self):
        sec = self.seconds
        sec = int(sec)
        min = self.minutes
        min = int(min)
        sec += 1
        
        if sec == 60:
            sec = 0
            min += 1
        
        if min == 30:
            self.fsm.s89()

        self.seconds = str(sec) if sec >= 10 else '0' + str(sec) 
        self.minutes = str(min) if min >= 10 else '0' + str(min)
        self.text = self.minutes + ":" + self.seconds
        EventManager.post_event("countdown", self.text)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
    
class TaskCanvas(BaseCanvas):
    
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        self.text = '0/10'
        self.count = 0
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        self.fsm = None
  
    def add_fsm(self, fsm):
        self.fsm = fsm    
    
    def plus(self):
        c = self.count
        c += 1
        self.count += 1
        Logger.log("task_advance" , str(self.count))
        
        if c != 10:
            EventManager.post_event("congratulations", -1)
            
        if c  > 10: return
        
        #Danger State I
        if c == 2:
            self.fsm.s12()
        elif c == 3:
            if self.fsm.is_s2:
                self.fsm.s23()

        #Danger State II
        elif c == 5:
            if self.fsm.is_s3:
                self.fsm.s34()
        elif c == 6:
            if self.fsm.is_s4:
                self.fsm.s45()

        #Danger State III
        elif c == 8:
            if self.fsm.is_s7:
                self.fsm.s78()
        elif c == 9:
            if self.fsm.is_s8:
                self.fsm.s89()
        
        #End
        elif c == 10:
            self.fsm.s910()

        self.text = "{count}/10".format(count=str(c))
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)

class ScoreCanvas(BaseCanvas):  
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        self.text = "1000"
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        
        EventManager.subscribe("task_count", self.subtract_score_task)
        
        EventManager.subscribe("step_error", self.subtract_score)
        EventManager.subscribe("step_error_danger", self.subtract_score)
        
        EventManager.subscribe("threshold_cross", self.subtract_score)
        EventManager.subscribe("threshold_cross_danger", self.subtract_score)
        EventManager.subscribe("collision_hit", self.subtract_score_hit)

        EventManager.subscribe("wrong_entry", self.subtract_score)
        EventManager.subscribe("duplicate_entry", self.subtract_score)
             
    def subtract_score_task(self, task_count):
        score = self.text
        score = int(score)
        score -= score_events["task_count"] * (10-int(task_count))
        self.text = str(score)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)

    def add_score(self, event_type):
        score = self.text
        score = int(score)
        score += score_events[event_type]
        self.text = str(score)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)

    def add_score_hit(self, hit_count):
        score = self.text
        score = int(score)
        score += score_events["collision_hit"] * int(hit_count)
        self.text = str(score)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        
    def subtract_score(self, event_type):
        score = self.text
        score = int(score)
        score -= score_events[event_type]
        self.text = str(score)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)

    def subtract_score_hit(self, hit_count):
        score = self.text
        score = int(score)
        score -= score_events["collision_hit"] * int(hit_count)
        self.text = str(score)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)

class CircleCanvas(BaseCanvas):
    def __init__(self, r, info_dict):
        super().__init__(r, info_dict)
        self.colors_dict = info_dict["colors"]
        self.color_lightgreen = self.colors_dict["light_green"]
        self.color_yellow = self.colors_dict["yellow"]
        self.color_orange = self.colors_dict["orange"]
        self.color_red = self.colors_dict["red"]
        self.state = "green"
        self.canvas.create_oval(1450, 75, 1430, 55, fill="green", outline="red")
        self.canvas.create_oval(5, 5, 200, 200, fill=self.color_lightgreen, outline=self.color_lightgreen,tags="circle")

        #self.canvas.create_rectangle(self.x, self.y, self.width, self.height, outline="black", width=2, fill="" )
        
        EventManager.subscribe("color_trans", self.color_transition)

    def color_transition(self, dummy = 0):
        if self.state == "green":
            self.canvas.delete("circle")
            self.canvas.create_oval(5, 5, 200, 200, fill=self.color_yellow, outline=self.color_yellow, tags="circle")
            self.state = "yellow"
        elif self.state == "yellow":
            self.canvas.delete("circle")
            self.canvas.create_oval(5, 5, 200, 200, fill=self.color_orange, outline=self.color_orange, tags="circle")
            self.state = "orange"

    def color_transition_reverse(self, dummy = 0):
        if self.state == "orange":
            self.canvas.delete("circle")
            self.canvas.create_oval(5, 5, 200, 200, fill=self.color_yellow, outline=self.color_yellow, tags="circle")
            self.state = "yellow"
        elif self.state == "yellow":
            self.canvas.delete("circle")
            self.canvas.create_oval(5, 5, 200, 200, fill=self.color_lightgreen, outline=self.color_lightgreen, tags="circle")
            self.state = "green"
        
        


            
        

import math
from textwrap import fill
from tkinter import *
import numpy
import threading
import random
from playsound import *
from event import *
import string
from logger import Logger
import global_variables
import time
from repeated_timer import RepeatedTimer

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


timer_canvas_info = {
    "x": 1725,
    "y": 75,
    "width": 200,
    "height": 50,
    "color": "blue",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}
timer_lbl_info = {
    "x": 1800,
    "y": 60,
    "width": 50,
    "height": 17,
    "color": "blue",
    "font": ('Helvetica', '12', 'bold'),
}
task_canvas_info = {
    "x": 1675,
    "y": 75,
    "width": 100,
    "height": 50,
    "color": "green",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}
task_lbl_info = {
    "x": 1700,
    "y": 60,
    "width": 50,
    "height": 17,
    "color": "green",
    "font": ('Helvetica', '12', 'bold'),

}

miss_canvas_agent_info = {
    "x": 1400,
    "y": 75,
    "width": 100,
    "height": 50,
    "color": "red",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}

miss_lbl_agent_info = {
    "x": 1425,
    "y": 60,
    "width": 50,
    "height": 17,
    "color": "red",
    "font": ('Helvetica', '12', 'bold'),
}


miss_canvas_operator_info = {
    "x": 1500,
    "y": 75,
    "width": 100,
    "height": 50,
    "color": "red",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}

miss_lbl_operator_info = {
    "x": 1515,
    "y": 60,
    "width": 70,
    "height": 17,
    "color": "red",
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
    "colors": {"light_green": '#03fc0f', "yellow": '#ecfc03', "orange": '#faa94d', "red": "#f70505"},
    "active": True
}




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
        if self.countdown != None:
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
        
        if global_variables.tutorial_mode:
            self.text = '0/5'
        else:
            self.text = '0/13'

        self.count = 0
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        self.fsm = None
  
    def add_fsm(self, fsm):
        self.fsm = fsm    
    
    def plus(self):
         
        c = self.count
        c += 1
        if c  > 13: return
        self.count += 1
        Logger.log("task_advance" , str(self.count))
        global_variables.task_advance = self.count
        
      
        
        if not global_variables.tutorial_mode:
            if c != 13:
                EventManager.post_event("congratulations", -1)
            
        #Danger State I
            if c == 2:
                self.fsm.s12()
            elif c == 4:
                if self.fsm.is_s2:
                    self.fsm.s23()

            #Danger State II
            elif c == 6:
                if self.fsm.is_s3:
                    self.fsm.s34()
            elif c == 8:
                if self.fsm.is_s4:
                    self.fsm.s45()

            if c == 9:
                #just to stop going forward, validating new codes will be denied until user makes a choice in
                if self.fsm.is_s6:
                    EventManager.post_event("try_again", -1)
                    
            #Danger State III
            elif c == 10:
                if self.fsm.is_s7:
                    self.fsm.s78()
            elif c == 12:
                if self.fsm.is_s8:
                    self.fsm.s89()
            
            #End
            elif c == 13:
                self.fsm.s910()
        else:
            
            if c != 5:
                EventManager.post_event("congratulations", -1)

            if c == 2:
                self.fsm.s12()
            elif c == 4:
                if self.fsm.is_s2:
                    self.fsm.s23()

            if c == 5:
                if self.fsm.is_s3:
                    self.fsm.s34()
            
            

        if global_variables.tutorial_mode:        
            self.text = "{count}/5".format(count=str(c))
            self.canvas.delete('all')
            self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        else:
            self.text = "{count}/13".format(count=str(c))
            self.canvas.delete('all')
            self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)

class MissCanavas(BaseCanvas):
    def __init__(self, r, dict_info, string):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        self.text = '0'
        self.user = string
        


        self.count = 0
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        self.fsm = None
  
        EventManager.subscribe("mistake", self.plus)

    def add_fsm(self, fsm):
        self.fsm = fsm    

    def plus(self, dummy = -1):

        if self.agent_is_doing_mistake_in_assisted() or self.operator_is_doing_mistake_in_manual():
            c = self.count
            c += 1
            if c  > 10: return
            self.count += 1

            self.text = "{count}".format(count=str(c))
            self.canvas.delete('all')
            self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        

    
    def operator_is_doing_mistake_in_manual(self):
        return not global_variables.jackalai_active and self.user == "operator"

    def agent_is_doing_mistake_in_assisted(self):
        return global_variables.jackalai_active and self.user == "agent"
            


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
        elif self.state == "orange":
            if global_variables.tutorial_mode:
                self.canvas.delete("circle")
                self.canvas.create_oval(5, 5, 200, 200, fill=self.color_red, outline=self.color_red, tags="circle")
                self.state = "red"

    def color_transition_reverse(self, dummy = 0):
        
        if self.state == "red":
                if global_variables.tutorial_mode:
                    self.canvas.delete("circle")
                    self.canvas.create_oval(5, 5, 200, 200, fill=self.color_orange, outline=self.color_orange, tags="circle")
                    self.state = "orange"
        elif self.state == "orange":
            self.canvas.delete("circle")
            self.canvas.create_oval(5, 5, 200, 200, fill=self.color_yellow, outline=self.color_yellow, tags="circle")
            self.state = "yellow"
        elif self.state == "yellow":
            self.canvas.delete("circle")
            self.canvas.create_oval(5, 5, 200, 200, fill=self.color_lightgreen, outline=self.color_lightgreen, tags="circle")
            self.state = "green"
        
        


            
        

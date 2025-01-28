import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/model/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/control/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/view/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/utils/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/test/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/data/')

import math
import textwrap
import tkinter as tk
import numpy as np
import playsound
import event_manager
import logger
import global_config as gv
import repeated_timer

class BaseCanvas():
    def __init__(self, r, info_dict):
        self.x = info_dict["x"]
        self.y = info_dict["y"]
        self.width = info_dict["width"]
        self.height = info_dict["height"]
        self.active = info_dict["active"]
        self.offset = 10
        
        self.canvas = tk.Canvas(r, bg=r.cget('bg'), width=self.width+self.offset, height=self.height+self.offset)
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
            self.a_up += np.deg2rad(self.angle_diff)
            self.a_left += np.deg2rad(self.angle_diff)
            self.a_right += np.deg2rad(self.angle_diff)
        elif string == "left":
            self.a_up -= np.deg2rad(self.angle_diff)
            self.a_left -= np.deg2rad(self.angle_diff)
            self.a_right -= np.deg2rad(self.angle_diff)
        
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


        event_manager.EventManager.subscribe("calibrate_pause", self.stop)
        event_manager.EventManager.subscribe("calibrate_start", self.start)

    def start(self, dummy = 0):
        if self.countdown == None:
            self.countdown = repeated_timer.RepeatedTimer(1, self.plus)
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


        self.seconds = str(sec) if sec >= 10 else '0' + str(sec) 
        self.minutes = str(min) if min >= 10 else '0' + str(min)
        self.text = self.minutes + ":" + self.seconds
        event_manager.EventManager.post_event("countdown", self.text)
        self.canvas.delete('all')
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
    
class TaskCanvas(BaseCanvas):
    
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        
        if gv.tutorial_mode:
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
        print("**********TASK ADVANCE********: " + str(c))
        c += 1
        if c  > 13: return
        self.count += 1
        logger.Logger.log("task_advance" , str(self.count))
        gv.task_advance = self.count
        
      
        
        if not gv.tutorial_mode:
            if c != 13:
                event_manager.EventManager.post_event("congratulations", -1)
            
        #Danger State I
            if c == 2:
                self.fsm.start_to_danger1_start()
            elif c == 4:
                if self.fsm.is_s2:
                    self.fsm.danger1_start_to_danger1_end()

            #Danger State II
            elif c == 6:
                if self.fsm.is_s3:
                    self.fsm.danger1_end_to_danger2_start()
            elif c == 8:
                if self.fsm.is_s4:
                    self.fsm.danger2_start_to_danger2_end()

            if c == 9:
                #just to stop going forward, validating new codes will be denied until user makes a choice in
                if self.fsm.is_s6:
                    event_manager.EventManager.post_event("try_again", -1)
                    
            #Danger State III
            elif c == 10:
                if self.fsm.is_s7:
                    self.fsm.decision_outcome_to_danger3_start()
            elif c == 12:
                if self.fsm.is_s8:
                    self.fsm.danger3_start_to_danger3_end()
            
            #End
            elif c == 13:
                self.fsm.danger3_end_to_termination()
        else:
            
            if c != 5:
                event_manager.EventManager.post_event("congratulations", -1)

            if c == 2:
                self.fsm.start_to_danger1_start()
            elif c == 4:
                if self.fsm.is_s2:
                    self.fsm.danger1_start_to_danger1_end()

            if c == 5:
                if self.fsm.is_s3:
                    self.fsm.danger1_end_to_danger2_start()
            
            

        if gv.tutorial_mode:        
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
  
        event_manager.EventManager.subscribe("mistake", self.plus)

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
        return not gv.jackalai_active and self.user == "operator"

    def agent_is_doing_mistake_in_assisted(self):
        return gv.jackalai_active and self.user == "agent"
            


class ScoreCanvas(BaseCanvas):  
    def __init__(self, r, dict_info):
        super().__init__(r, dict_info)
        self.color = dict_info["color"]
        self.font = dict_info["font"]
        self.text = "1000"
        self.canvas.create_text(self.width/2, self.height/2, text= self.text, fill= self.color, font= self.font)
        
        event_manager.EventManager.subscribe("task_count", self.subtract_score_task)
        
        event_manager.EventManager.subscribe("step_error", self.subtract_score)
        event_manager.EventManager.subscribe("step_error_danger", self.subtract_score)
        
        event_manager.EventManager.subscribe("threshold_cross", self.subtract_score)
        event_manager.EventManager.subscribe("threshold_cross_danger", self.subtract_score)
        event_manager.EventManager.subscribe("collision_hit", self.subtract_score_hit)

        event_manager.EventManager.subscribe("wrong_entry", self.subtract_score)
        event_manager.EventManager.subscribe("duplicate_entry", self.subtract_score)
             
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
        
        event_manager.EventManager.subscribe("color_trans", self.color_transition)

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
            if gv.tutorial_mode:
                self.canvas.delete("circle")
                self.canvas.create_oval(5, 5, 200, 200, fill=self.color_red, outline=self.color_red, tags="circle")
                self.state = "red"

    def color_transition_reverse(self, dummy = 0):
        
        if self.state == "red":
                if gv.tutorial_mode:
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
        
        


            
        

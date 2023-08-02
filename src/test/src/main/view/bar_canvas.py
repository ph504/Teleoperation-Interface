from event import EventManager
from canvas import BaseCanvas
import playsound
import global_variables
from logger import Logger
from repeated_timer import RepeatedTimer
import time

bar_canvas_info_main = {
    "x": 560,
    "y": 70,
    "width": 800,
    "height": 20,

    "bar_defaultpercent_slow": 40/100,
    "bar_defaultpercent_fast": 40/100,

    "line_thresholdpercent": 80/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "blue",
    "line_color": "red",
    "line_width": 2,

    "move_interval_slow": 0.7,
    "progress_step_slow": 0.5,

    "move_interval_fast": 0.7,
    "progress_step_fast": 0.5,

    "active": True

}
bar_canvas_info1 = {
    "x": 560,
    "y": 30,
    "width": 800,
    "height": 20,

    "bar_defaultpercent_slow": 20/100,
    "bar_defaultpercent_fast": 50/100,

    "line_thresholdpercent": 85/100,


    "outline_color": "black",
    "outline_width": 2,
    "color": "green",
    "line_color": "red",
    "line_width": 2,

    "move_interval_slow": 2.5,
    "progress_step_slow": 3,

    "move_interval_fast": 0.6,
    "progress_step_fast": 10,

    "active": False

}
bar_canvas_info2 = {
    "x": 560,
    "y": 60,
    "width": 800,
    "height": 20,

   

    "bar_defaultpercent_slow": 20/100,
    "bar_defaultpercent_fast": 50/100,

    "line_thresholdpercent": 80/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "green",
    "line_color": "red",
    "line_width": 2,

    "move_interval_slow": 1,
    "progress_step_slow": 1,

    "move_interval_fast": 0.4,
    "progress_step_fast": 8,
    "active": False

}
bar_canvas_info3 = {
    "x": 560,
    "y": 90,
    "width": 800,
    "height": 20,

    "bar_defaultpercent_slow": 20/100,
    "bar_defaultpercent_fast": 50/100,

    "line_thresholdpercent": 90/100,
    "outline_color": "black",
    "outline_width": 2,
    "color": "green",
    "line_color": "red",
    "line_width": 2,
    "move_interval_slow": 2,
    "progress_step_slow": 2.5,

    "move_interval_fast": 0.5,
    "progress_step_fast": 10,
    "active": False

}



class BarCanvas(BaseCanvas): 
    danger_mode = None
    danger_count = 0
    manual_mode = None
    bar_tag = 0
    def __init__(self, r, info_dict, danger):
        super().__init__(r,info_dict)
       
       
        self.bar_defaultpercent_slow = info_dict["bar_defaultpercent_slow"]
        self.bar_defaultpercent_fast = info_dict["bar_defaultpercent_fast"]

        self.curr_bar_defaultpercent = self.bar_defaultpercent_slow
        self.bar_percent = self.curr_bar_defaultpercent


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
        self.bar_tag = BarCanvas.bar_tag
        BarCanvas.bar_tag += 1
       
        
        self.move_interval_slow = info_dict["move_interval_slow"]
        self.move_interval_fast = info_dict["move_interval_fast"]
       
        self.progress_step_slow = info_dict["progress_step_slow"]
        self.progress_step_fast = info_dict["progress_step_fast"]

        self.curr_move_interval = self.move_interval_slow
        self.curr_progress_step = self.progress_step_slow

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

        EventManager.subscribe("bar_fast_mode", self.bar_mode_fast)
        EventManager.subscribe("bar_slow_mode", self.bar_mode_slow)
        EventManager.subscribe("bar_ultra_mode", self.bar_mode_ultra)
    

        EventManager.subscribe("start_move_bars", self.random_movement)
        EventManager.subscribe("stop_move_bars", self.stop_move_bars)

        EventManager.subscribe("move_bar_backward", self.normal_cooldown)
    
    def start(self):
        print("it should start the repeated time!")
        
        #self.secondary_task = RepeatedTimer(10, self.random_movement)
           
    def move_bar(self,string):   
        #just to prevent danger bars being active while normal is active (and vice versa) 
        
        if (self.is_danger and BarCanvas.danger_mode) or (not self.is_danger and not BarCanvas.danger_mode):
            
            self.canvas.delete(self.tag_bar,self.tag_line)
            if string == "left" and self.bar_percent > 0: self.bar_percent -= self.curr_progress_step / 100
            elif string == "right" and self.bar_percent < 100: self.bar_percent += self.curr_progress_step / 100
            
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
        elif self.passed and self.bar_percent < self.line_thresholdpercent:
            self.passed = False
            return
        
        # check to see if the user ignored and the bar is just keep going 
        elif self.passed and self.bar_percent > self.line_thresholdpercent + self.curr_progress_step/100:
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill="red", tags=self.tag_bar)
            self.canvas.create_line(self.width * self.line_thresholdpercent, 0, self.width * self.line_thresholdpercent, self.height, fill="blue", width=self.line_width, tags=self.tag_line)
            playsound("/home/pouya/catkin_ws/src/test/src/sounds/error.wav", block=False)
            
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

    def bar_mode_fast(self, bar_tg):
        
        if self.bar_tag == bar_tg:
            print("FAST MODE!")
            
            self.curr_move_interval = 0.15
            self.curr_progress_step = 15
            self.repeat_moving.stop()
            self.repeat_moving.change_interval(self.curr_move_interval)
            self.repeat_moving.change_args("right")
            self.repeat_moving.start()

    def bar_mode_slow(self,bar_tg):
        if self.bar_tag == bar_tg:
            print("SLOW MODE")
            self.curr_bar_defaultpercent = self.bar_defaultpercent_slow
            self.curr_move_interval = self.move_interval_slow
            self.curr_progress_step = self.progress_step_slow    
            
            self.repeat_moving.stop()
            self.repeat_moving.change_interval(self.curr_move_interval)
            self.repeat_moving.change_args("right")
            self.repeat_moving.start()

    def bar_mode_ultra(self,bar_tag):

        if self.bar_tag == bar_tag:
            print("ULTRA MODE!")
            self.bar_percent = self.line_thresholdpercent
            self.curr_move_interval = 0.6
            self.curr_progress_step = 3
            self.repeat_moving.stop()
            self.repeat_moving.change_interval(self.curr_move_interval)
            self.repeat_moving.change_args("right")
            self.repeat_moving.start()
     
    def reset_button(self):
        EventManager.post_event("bar_slow_mode", self)
        if self.passed == False:
            EventManager.post_event("error_push")
            return
        else:
            self.passed = False
            if global_variables.tutorial_mode:
                playsound("/home/pouya/catkin_ws/src/test/src/sounds/beep.wav", block=False) 
            elif not global_variables.jackalai_active or not self.red_mode:
                playsound("/home/pouya/catkin_ws/src/test/src/sounds/beep.wav", block=False) 
            
            self.red_mode = False
            
            if not self.is_danger:
                self.bar_percent = 50/100
            else:
                #self.bar_percent = random.randint(20, self.line_thresholdpercent * 100) / 100
                self.bar_percent = self.curr_bar_defaultpercent
            
            
            self.canvas.delete(self.tag_bar,self.tag_line)
            self.canvas.create_rectangle(2,2, self.width * self.bar_percent, self.height, fill=self.bar_color, tags=self.tag_bar)
            self.canvas.create_line(self.width*self.line_thresholdpercent,0,self.width*self.line_thresholdpercent,self.height, fill=self.line_color, width=self.line_width, tags=self.tag_line)

    def reset(self):
        self.passed = False
        self.bar_percent = self.curr_bar_defaultpercent
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
                    self.repeat_moving.change_interval(interval)
                    self.repeat_moving.change_args(string)
                    self.repeat_moving.start()
                else:
                    
                    self.repeat_moving = RepeatedTimer(interval, self.move_bar, string)  
        else:
            if self.repeat_moving is not None:
                self.repeat_moving.stop()
                self.repeat_moving.change_interval(interval)
                self.repeat_moving.change_args(string)
                self.repeat_moving.start()
            else:
                self.repeat_moving = RepeatedTimer(interval, self.move_bar, string)  
    
    def stop_move_bars(self, dummy = -1):
        self.repeat_moving.stop()
    
    def normal_cooldown(self, bar):
        print("go back! --- normal cooldown")
        if self.bar_tag == bar.bar_tag:
            self.move_left()
            time.sleep(1)
            if self.bar_percent < 50/100:
                self.move_right()
            else:
                time.sleep(15)
                self.move_right()
    
    def move_left(self, dummy = -1):
        self.repeat_moving.stop()
        self.repeat_moving.change_interval(self.curr_move_interval)
        self.repeat_moving.change_args("left")
        self.repeat_moving.start()
    
    def move_right(self, dummy = -1):
        self.repeat_moving.stop()
        self.repeat_moving.change_interval(self.curr_move_interval)
        self.repeat_moving.change_args("right")
        self.repeat_moving.start()

    def random_movement(self, dummy = -1):
        self.move_bar_repeat("right", self.curr_move_interval)

from tkinter import Label
from PIL import Image, ImageTk
import time
import threading
import event
from canvas import RepeatedTimer
import global_variables

javatar_info = {
    "x": 460,
    "y": 800,
    "width": 200,
    "height": 180,
}


javatar_images = {
    "default" : "/home/pouya/catkin_ws/src/test/src/images/JACKEL/default/IDLE_01.png",
    "default-talking": "/home/pouya/catkin_ws/src/test/src/images/JACKEL/default/IDLE_05.png",
    "default-blink": "/home/pouya/catkin_ws/src/test/src/images/JACKEL/default/IDLE_04.png",
    "default-left": "/home/pouya/catkin_ws/src/test/src/images/JACKEL/default/IDLE_02.png",
    "default-right": "/home/pouya/catkin_ws/src/test/src/images/JACKEL/default/IDLE_03.png",
    "happy" : "/home/pouya/catkin_ws/src/test/src/images/JACKEL/happy/IDLE_17.png",
    "happy-blink": "/home/pouya/catkin_ws/src/test/src/images/JACKEL/happy/IDLE_20.png",
    "sad" : "/home/pouya/catkin_ws/src/test/src/images/JACKEL/sad/IDLE_09.png",
    "sad-blink": "/home/pouya/catkin_ws/src/test/src/images/JACKEL/sad/IDLE_12.png",
    "sad-talking": "/home/pouya/catkin_ws/src/test/src/images/JACKEL/sad/IDLE_13.png",
    "angry": "/home/pouya/catkin_ws/src/test/src/images/JACKEL/angry/IDLE_21.png",
    "angry-blink": "/home/pouya/catkin_ws/src/test/src/images/JACKEL/angry/IDLE_24.png",
    "nonsocial": "/home/pouya/catkin_ws/src/test/src/images/non_social.png"

}


class Avatar():
    
    def __init__(self,root , avatar_info, avatar_images):
            self.x = avatar_info["x"]
            self.y = avatar_info["y"]
            self.width = avatar_info["width"]
            self.height = avatar_info["height"]
            self.image = Image.open(avatar_images["default"]).resize((self.width,self.height), Image.ANTIALIAS) if global_variables.social_mode is True else Image.open(avatar_images["nonsocial"]).resize((self.width,self.height), Image.ANTIALIAS)
            self.imagetk = ImageTk.PhotoImage(self.image)
            self.label = Label(root)
            self.label.config(image = self.imagetk)
            self.label.image = self.imagetk
            self.label.place(x = self.x ,y = self.y ,width = self.width ,height = self.height)
            self.state = "default"
            self.repeated_talking = None
            self.repeated_talking_sad = None
            self.first_time = True
            self.count_blink = 0
            self.sad_mode = False
            self.first_time_sad = True
            if global_variables.social_mode:
                event.EventManager.subscribe("collision", self.change_image_hit)
                event.EventManager.subscribe("mistake", self.change_image_hit)
                event.EventManager.subscribe("congratulations", self.change_image_congratulations)
                event.EventManager.subscribe("talking_started", self.change_image_talking)
                event.EventManager.subscribe("talking_ended", self.end_talking)
                event.EventManager.subscribe("talking_started_sad", self.change_image_talking_sad)
                event.EventManager.subscribe("stop_talking", self.end_talking)
                self.idle_event = threading.Event()
                self.idle_event.set()
                t = threading.Thread(target=self.idle_loop)
                t.start()

           

    def idle_loop(self): 
            
        while True: 
           
            time.sleep(10)
            
            if not self.idle_event.is_set(): 
                 self.idle_event.wait()
                 continue
            else: self.change_image('default-blink')
            time.sleep(0.5)
            if not self.idle_event.is_set(): 
                 self.idle_event.wait()
                 continue
            else: self.change_image('default-left')
            time.sleep(0.5)
            if not self.idle_event.is_set(): 
                 self.idle_event.wait()
                 continue
            else: self.change_image('default-blink')
            time.sleep(0.5)
            if not self.idle_event.is_set(): 
                 self.idle_event.wait()
                 continue
            else: self.change_image('default-right')
            time.sleep(0.5)
            if not self.idle_event.is_set(): 
                 self.idle_event.wait()
                 continue
            else: self.change_image('default-blink')
            time.sleep(0.5)
            if not self.idle_event.is_set(): 
                 self.idle_event.wait()
                 continue
            else: self.change_image('default')

    def change_image(self,state):
        self.image = Image.open(javatar_images[state]).resize((self.width,self.height), Image.ANTIALIAS)
        self.state = state
        self.imagetk = ImageTk.PhotoImage(self.image)
        self.label.config(image = self.imagetk)
        self.label.image = self.imagetk
   
    def change_image_temp(self,state):
        def swap_images(s, p_s):
            self.change_image(s)
            time.sleep(10)
            self.change_image(p_s)
        prev_state = self.state
        t = threading.Thread(target=swap_images, args=(state, prev_state))
        t.start()


    def change_image_talking(self,dummy=0):
        self.idle_event.clear()
        def swap_images():
            self.change_image("default-blink") if self.count_blink % 3 == 0 else self.change_image("default")
            self.count_blink += 1
            time.sleep(0.5)
            self.change_image("default-talking")
        if self.first_time:
            self.first_time = False
            def wait_start():
                time.sleep(1.5)
                self.repeated_talking = RepeatedTimer(2, swap_images)
            t= threading.Thread(target=wait_start)
            t.start()
        else:
           swap_images()
           self.repeated_talking.start()
    

    def change_image_talking_sad(self,dummy=0):
            self.idle_event.clear()
            self.sad_mode = True
            def swap_images():
                self.change_image("sad-blink") if self.count_blink % 3 == 0 else self.change_image("sad")
                self.count_blink += 1
                time.sleep(0.5)
                self.change_image("sad-talking")
            if self.first_time_sad:
                self.first_time_sad = False
                def wait_start():
                    swap_images()
                    self.repeated_talking_sad  = RepeatedTimer(2, swap_images)
                t= threading.Thread(target=wait_start)
                t.start()
            else:
                swap_images()
                self.repeated_talking_sad.start()
    
    
    def end_talking(self,talkmode):
        
        def func():
            if self.sad_mode == True:
                    self.change_image("sad")
                    self.repeated_talking_sad.stop()
                    time.sleep(3)
                    self.change_image("default")
                    self.sad_mode = False
            else:
                    
                    self.repeated_talking.stop()
                    time.sleep(0.5)
                    self.change_image("default")

        if talkmode:
            self.idle_event.set()
            x = threading.Thread(target=func)
            x.start()
        else:
            pass         
           
    def change_image_hit(self, dummy=0):
        self.idle_event.clear()
        def swap_images(s, _s, p_s):
            self.change_image(s)
            time.sleep(2)
            self.change_image(_s)
            time.sleep(0.5)
            self.change_image(s)
            time.sleep(2)
            self.change_image(p_s)
            self.idle_event.set()
        prev_state = self.state
        t = threading.Thread(target=swap_images, args=("sad", "sad-blink", prev_state))
        t.start()
             
    def change_image_congratulations(self, dummy=0):
        self.idle_event.clear()
        def swap_images(s, _s, p_s):
            self.change_image(s)
            time.sleep(2)
            self.change_image(_s)
            time.sleep(0.5)
            self.change_image(s)
            time.sleep(2)
            self.change_image(p_s)
            self.idle_event.set()
        prev_state = self.state
        t = threading.Thread(target=swap_images, args=("happy","happy-blink", prev_state))
        t.start()

    def change_image_happy(self, dummy=0):
            self.idle_event.clear()
            def swap_images(s, _s, p_s):
                self.change_image(s)
                time.sleep(2)
                self.change_image(_s)
                time.sleep(0.5)
                self.change_image(s)
                time.sleep(2)
                self.change_image(p_s)
                self.idle_event.set()
            prev_state = self.state
            t = threading.Thread(target=swap_images, args=("happy","happy-blink", prev_state))
            t.start()

        
        

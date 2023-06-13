from tkinter import Label
from PIL import Image, ImageTk
import time
import utils
from tkinter import Tk
import csv
from collections import deque


javatar_info = {
    "x": 460,
    "y": 800,
    "width": 200,
    "height": 180,
}

class AvatarView():
    def __init__(self, frame,  dict_info,social) -> None:
        self.frame = frame
        self.x = dict_info["x"]
        self.y = dict_info["y"]
        self.width = dict_info["width"]
        self.height = dict_info["height"]
        self.label = Label(self.frame)
        self.label.place(x = self.x, y = self.y, width = self.width, height = self.height)
        self.social = social

        self.non_social_image = Image.open("/home/pouya/catkin_ws/src/test/src/images/non_social.png").resize((self.width,self.height), Image.ANTIALIAS)
        self.curr_image = Image.open("/home/pouya/catkin_ws/src/test/src/images/JACKEL/happy/IDLE_19.png").resize((self.width,self.height), Image.ANTIALIAS)
        self.imagetk = ImageTk.PhotoImage(self.curr_image)

        self.label.configure(image=self.imagetk)

        self.display()

    def display(self):
        
        if self.social:
            image = self.curr_image.resize((self.width,self.height), Image.ANTIALIAS)
        else:
            image = self.non_social_image

        self.imagetk = ImageTk.PhotoImage(image)
        self.label.config(image = self.imagetk)
        Tk.after(self.frame, 100, self.display)
   
    def set_image(self, image):
        self.curr_image = image

#TODO: Create        
class AvatarModel():
    def __init__(self, csv_idle_filepath, csv_talking_filepath, csv_reactive_filepath) -> None:
        
        self.csv_idle_filepath = csv_idle_filepath
        self.csv_talking_filepath = csv_talking_filepath
        self.csv_reactive_filepath = csv_reactive_filepath
    
    def find_obj(self,key):
       if key[0] == 't':
           with open(self.csv_talking_filepath, mode='r', newline='') as csv_f:
                csv_reader = csv.DictReader(csv_f)
                for row in csv_reader:
                    if row['key'] == key:
                        return AvatarTalking(row)                   
       elif key[0] == 'i':
           with open(self.csv_idle_filepath, mode='r', newline='') as csv_f:
                csv_reader = csv.DictReader(csv_f)
                for row in csv_reader:
                    if row['key'] == key:
                        return AvatarIdle(row)          
       elif key[0] == 'r':
           with open(self.csv_reactive_filepath, mode='r', newline='') as csv_f:
                csv_reader = csv.DictReader(csv_f)
                for row in csv_reader:
                    if row['key'] == key:
                        return AvatarReactive(row)

#TODO: Avatar Object should be created in the model not in controller
class AvatarController(object):
    def __init__(self, frame, model: AvatarModel, view: AvatarView) -> None:
        self.frame = frame
        self.model = model
        
        self.view = view

        self.curr_avatar = None
        
        self.avatar_stack = deque()
        self.idle_avatar = self.model.find_obj('i_default')
        
        self.update_view()
        
    def update_view(self):

        #if it's in complete idle mode (no new dialogues)
        if not self.avatar_stack and self.curr_avatar is None:
            img = self.idle_avatar.get_currimage()
            self.view.set_image(img)
        
        # if a new avatar comes up 
        if self.avatar_stack and self.curr_avatar == None:
            
            self.curr_avatar = self.avatar_stack.pop()
        
        #if in the middle of a dialogue, a new one comes up
        if self.avatar_stack and self.curr_avatar != None:
            temp = self.curr_avatar
            self.curr_avatar = self.avatar_stack.pop()
            self.avatar_stack.append(temp)

        #if the current dialogue is finished
        if self.curr_avatar != None and self.curr_avatar.finished:
            self.curr_avatar = None

        #if a dialogue is running
        if self.curr_avatar != None:
            img = self.curr_avatar.get_currimage()
            self.view.set_image(img)

        Tk.after(self.frame, 100, self.update_view)

    def set_avatar(self, key):
        avatar_obj  = self.model.find_obj(key)
        self.avatar_stack.append(avatar_obj)

#TODO: Avatar object Should get a row and everything be         
class AvatarObject():
    def __init__(self) -> None:
        self.started = False
        self.finished = False
        self.curr_img = None
        self.type = None

    def change_currimg(self, img):
        self.curr_img = img

    def get_currimage(self):
        return self.curr_img

    def animate(self):
        pass

class AvatarReactive(AvatarObject):
    def __init__(self, dict_info) -> None:
        super().__init__()

        self.type = "Reactive"
        self.emotion = dict_info['emotion']
        self.reaction_path = dict_info['reaction_path']
        self.reaction_time = float(dict_info['reaction_time'])
        self.blink_path = dict_info['blink_path']
        self.blink_time = float(dict_info['blink_time'])
        
        self.reaction_img = Image.open(self.reaction_path)
        self.blink_img = Image.open(self.blink_path)

        
        self.animate()
    
    @utils.thread
    def animate(self):
        
        self.started = True

        self.change_currimg(self.reaction_img)

        time.sleep(self.reaction_time)

        self.change_currimg(self.blink_img)

        time.sleep(self.blink_time)

        self.change_currimg(self.reaction_img)

        time.sleep(self.reaction_time)
        
        self.finished = True

class AvatarTalking(AvatarObject):
    def __init__(self, dict_info) -> None:
        super().__init__()        

        self.type = "Talking"
        self.emotion = dict_info['emotion']
        self.default_path = dict_info['default_path']
        self.talking_path = dict_info['talking_path']
        self.blink_path = dict_info['blink_path']
         
        self.talking_time = float(dict_info['talking_time'])
        self.interval_time = float(dict_info['interval_time'])
        self.blink_countmax = float(dict_info['blink_countmax'])

        self.default_img = Image.open(self.default_path)
        self.blink_img = Image.open(self.blink_path)
        self.talking_img = Image.open(self.talking_path)

        self.count_blink = 0

        self.animate()

    @utils.thread
    def animate(self):
            self.change_currimg(self.default_img)
            while True:
                self.change_currimg(self.blink_img) if self.count_blink % self.blink_countmax == 0 else self.change_currimg(self.default_img)
                self.count_blink += 1
                time.sleep(self.talking_time)
                self.change_currimg(self.talking_img)
                time.sleep(self.interval_time)

class AvatarIdle(AvatarObject):
    def __init__(self, dict_info) -> None:
        super().__init__()
        
        self.type = "Idle"
        self.emotion = dict_info['emotion']
        self.default_path = dict_info['default_path']
        self.left_path = dict_info['left_path']
        self.right_path = dict_info['right_path']
        self.blink_path = dict_info['blink_path']

        self.idleloop_time = float(dict_info['idleloop_time'])
        self.blink_time = float(dict_info['blink_time'])


        self.default_img = Image.open(self.default_path)
        self.left_img = Image.open(self.left_path)
        self.right_img = Image.open(self.right_path)
        self.blink_img = Image.open(self.blink_path)


        

        self.animate()
        
    @utils.thread
    def animate(self):
      
        self.change_currimg(self.default_img)

        while True: 

            time.sleep(self.idleloop_time)

            self.change_currimg(self.blink_img)

            time.sleep(self.blink_time)

            self.change_currimg(self.left_img)

            time.sleep(self.blink_time)

            self.change_currimg(self.blink_img)

            time.sleep(self.blink_time)

            self.change_currimg(self.right_img)

            time.sleep(self.blink_time)

            self.change_currimg(self.blink_img)

            time.sleep(self.blink_time)

            self.change_currimg(self.default_img)

    
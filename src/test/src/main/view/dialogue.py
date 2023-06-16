from tkinter import Label, Button, ACTIVE, DISABLED
import time
from tkinter import Tk
import utils
import csv
from collections import deque
import threading
import random
import playsound

dialogueview_info = {
    "x": 660,
    "y": 800,
    "width": 800,
    "height": 180,
    "font": ('Calibri',12, 'bold', 'italic'),
    "bg": '#d9d7bd',
    "wraplength": 800,
    

    "btn1_info": {
        "x": 1250,
        "y": 940,
        "text": "Button 1", 
        "width": 100,
        "height": 30,
        
    },

    "btn2_info": { 
        "x": 1350,
        "y": 940,
        "text": "Button 2",
        "width": 100,
        "height": 30,
        
    },

    "btn_info": {   
        "x": 1300,
        "y": 940,
        "text": "Button",
        "width": 100,
        "height": 30,
    },

    
   

}


dbox_info = {
    "x": 660,
    "y": 800,
    "width": 800,
    "height": 180
}

class BaseButton():
    def __init__(self, r, info_dict, activate=True, enable = True):
        self.x = info_dict["x"]
        self.y = info_dict["y"]
        self.width = info_dict["width"]
        self.height = info_dict["height"]
        self.text = info_dict["text"]
        self.button = Button(r, width= self.width, height=self.height, 
            text= self.text)
        
        if enable == True: self.enable()
        elif enable == False: self.disable()
        
        
        if activate == True: self.activate()
        elif activate == False: self.deactivate()
        
    def add_event(self, event):
            self.button.config(command=event)

    def enable(self):
            self.button.config(state=ACTIVE)

    def disable(self):
            self.button.config(state=DISABLED)
      
    def deactivate(self):
        self.button.place(x = 5000, y = self.y, width=self.width, height=self.height)
    
    def activate(self):
        self.button.place(x = self.x, y = self.y, width=self.width, height=self.height)

    def set_text(self, text):
         self.button.config(text= text)
         self.text = text

class DialogueView():
    
    def __init__(self, frame,  dict_info) -> None:
        
        #box data
        self.frame = frame
        self.x = dict_info["x"]
        self.y = dict_info["y"]
        self.width = dict_info["width"]
        self.height = dict_info["height"]
        self.font =  dict_info["font"]
        self.bg = dict_info["bg"]
        self.wraplength = dict_info["wraplength"]
        
        self.dbox = Label(frame,font=self.font, bg=self.bg, wraplength=self.wraplength)
        self.dbox.place(x = self.x, y = self.y, width= self.width, height=self.height)
        
        self.button_press = False
        self.button_press_1 = False
        self.button_press_2 = False
        self.sentence = ""
        self.button_press_name = None
        

        self.button_mode = 0 #0 to 2 for each button

        self.btn1 = BaseButton(self.frame, dict_info["btn1_info"], activate=False, enable= False)
        self.btn2 = BaseButton(self.frame, dict_info["btn2_info"], activate=False, enable= False)
        self.btn =  BaseButton(self.frame, dict_info["btn_info"], activate=False, enable=False)
    
        self.display()
    
    def set_sentence(self, string):
        self.sentence = string

    def display(self):
        self.dbox.config(text = self.sentence)
        Tk.after(self.frame, 100, self.display)
    
    # a lousy way to find out which button is pressed
    
    #btn 
    def button_press_event(self):
        self.button_press = True 
        self.button_press_name = self.btn.text

    #btn 1
    def button_press_event_1(self):
        self.button_press_1 = True 
        self.button_press_name_1 = self.btn1.text

    #btn 2
    def button_press_event_2(self):
        self.button_press_2 = True
        self.button_press_name_2 = self.btn2.text   
         
    def init_buttons(self,num, text = "", text1 = "", text2= ""):
        if num == 0:
              return
        elif num == 1:
              self.btn.activate()
              self.btn.set_text(text)
              self.btn.add_event(self.button_press_event)
        elif num == 2:
             self.btn1.activate()
             self.btn1.set_text(text1)
             self.btn1.add_event(self.button_press_event_1)
             self.btn2.activate()
             self.btn2.set_text(text2)
             self.btn2.add_event(self.button_press_event_2)

    def hide_buttons(self, num):
        if num == 0:
            return
        elif num == 1:
            self.btn.deactivate()
              
        elif num == 2:
            self.btn1.deactivate()
            self.btn2.deactivate()
         
    def enable_buttons(self, num):
        if num == 0:
            return
        elif num == 1:
            self.btn.enable()
        elif num == 2:
            self.btn1.enable()
            self.btn2.enable()
    
    def disable_buttons(self, num):
        if num == 0:
              return
        elif num == 1:
              self.btn.disable()
        elif num == 2:
             self.btn1.disable()
             self.btn2.disable()

class DialogueObject():
    def __init__(self, dict_info):
        
        self.key = dict_info["key"]
        self.button_num = int(dict_info["btn_num"])
        self.button_title = dict_info["btn_title"]
        self.button1_title = dict_info["btn1_title"]
        self.button2_title = dict_info["btn2_title"]   
        self.random = eval(dict_info["random"].lower().capitalize()) #choose text randomly from the list of texts or not
 

        if self.random:
            self.full_text = self.return_random_d(dict_info["text"])
        else: 
            self.full_text = dict_info["text"] 

        self.str_index= 0
        self.shown_text = ""
        self.remaining_text = self.full_text
        
        self.wipe_with_button = eval(dict_info["wipe_with_button"].lower().capitalize())
       
        self.wipe_time = int(dict_info["wipe_time"])

        self.wait_before_start = int(dict_info["wait_before_start"])
        self.space_pause = 0.2
        self.letter_pause = 0.1
        
        self.started = False
        self.showing = False
        self.stopped = False
        self.finished = False
        self.wait_for_button = False
        self.queue_flag = None
        
        self.event = threading.Event()
        self.event.set()
      

    def return_random_d(self,string):
            list = string.split(",")

            if len(list) == 1:
                return list[0]
            else:
                rand = random.randint(0, len(list)-1)
                return list[rand]

    def update_texts(self):
        
        self.str_index += 1
        self.shown_text = self.full_text[:self.str_index] 
        self.remaining_text = self.full_text[self.str_index:]

    @utils.thread
    def letterbyletter(self):
        
        time.sleep(self.wait_before_start)

        self.showing = True

        for l in self.full_text:
            self.event.wait()
            if l == " ":   
                time.sleep(self.space_pause)
            else:
                playsound.playsound("/home/pouya/catkin_ws/src/test/src/sounds/bleep_sliced.wav")
            
            self.update_texts()
        
        if not self.wipe_with_button: 
           self.wipe(self.wipe_time)
        else:
            self.wait_for_button = True
               
        self.showing = False
        self.stopped = True
        
    def pause_letterbyletter(self):  
        self.showing = False
        self.queue_flag = True  
        self.event.clear()

    def start_letterbyletter(self):
        if not self.started:
            self.started = True
            self.letterbyletter()
        else:
            if not self.wait_for_button:
                self.showing = True

        self.event.set()
       
    @utils.thread
    def wipe(self, wipe_time):
        time.sleep(wipe_time)
        self.shown_text = " "
        time.sleep(0.1)
        self.finished = True

class DialogueModel():
     def __init__(self, frame,  csv_filepath) -> None:
          self.frame = frame
          self.csv_filepath = csv_filepath

     def find_obj(self, key):
          with open(self.csv_filepath, mode='r', newline='') as csv_f:
               csv_reader = csv.DictReader(csv_f)
               line_count = 0
               for row in csv_reader:
                        if row['key'] == key:
                             return DialogueObject(row)

class DialogueController(object):
    
    def __init__(self, frame, model: DialogueModel, view: DialogueView):
            
            self.frame = frame 
            self.view = view
            self.model = model
            self.curr_dialogue = None
            self.dialogue_stack = deque()
            self.button_press = False
            self.btn_press_name = None
            
            
            self.update_btnpress()
            self.update_view()
            
    def update_btnpress(self):

       if self.view.button_press:
            self.button_press = True
            self.btn_press_name = self.view.button_press_name
            self.view.button_press = False
        
       if self.view.button_press_1:
            self.button_press = True
            self.btn_press_name = self.view.button_press_name_1
            self.view.button_press_1 = False

       if self.view.button_press_2:
            self.button_press = True
            self.btn_press_name = self.view.button_press_name_2
            self.view.button_press_2 = False
        

       Tk.after(self.frame, 100, self.update_btnpress)

    def update_view(self):

        #if there is no dialogue
        if not self.dialogue_stack and self.curr_dialogue is None:
            self.view.set_sentence('')

        #if there is a new dialogue
        if self.dialogue_stack and self.curr_dialogue is None: 
            self.curr_dialogue = self.dialogue_stack.pop()
            self.curr_dialogue.start_letterbyletter()

        #if in the middle of a dialogue, a "new" dialogue comes up that it's queue flag is not set (means it hasn't been used)
        #i did that because of what bug? because when the new bialogue came and then it finished, it again put it on the stack after the bigger one is finished.
        #since it's dialogue dependent ... makes sense to put that in avalogue
        if self.dialogue_stack and self.curr_dialogue != None and not self.dialogue_stack[0].queue_flag:
            self.curr_dialogue.pause_letterbyletter()
            temp = self.curr_dialogue
            self.curr_dialogue = self.dialogue_stack.pop()
            self.curr_dialogue.start_letterbyletter()
            self.dialogue_stack.append(temp)


        #If the current dialogue is not finished (it is showing as well)
        if self.curr_dialogue is not None and not self.curr_dialogue.finished:
            self.view.set_sentence(self.curr_dialogue.shown_text)
      
        #If dialogue is done showing and waiting for buttons (avatars should be idle this time)
        if self.curr_dialogue is not None and not self.curr_dialogue.showing:
            self.view.enable_buttons(self.curr_dialogue.button_num)
        
        #if the current dialogue is finished (for non-button mode, it's wiped actually) , Avatar should be idle here
        if self.curr_dialogue is not None and self.curr_dialogue.finished:
            self.curr_dialogue = None

        #if the current dialogue is finished (for button mode) 
        if self.button_press:
            self.view.hide_buttons(self.curr_dialogue.button_num)
            func = utils.find_func(self.btn_press_name)
            print(func)
            self.curr_dialogue = None
            self.button_press = False
            self.btn_press_name = None
            func()

        Tk.after(self.frame, 100, self.update_view)

    def set_dialogue(self, key):
        dialogue_obj = self.model.find_obj(key)
        
        self.view.init_buttons(dialogue_obj.button_num, 
                               dialogue_obj.button_title,
                                dialogue_obj.button1_title,
                                dialogue_obj.button2_title)
        
        self.dialogue_stack.append(dialogue_obj)
        


    
        



        


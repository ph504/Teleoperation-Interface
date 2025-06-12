from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

from tkinter import Label, Button, ACTIVE, DISABLED
from tkinter import font as tkFont
import time
from tkinter import Tk
from main.utils import utils
import csv
from collections import deque
import threading
import random
import playsound
from main.data import global_config
from main.control import event_manager
from main.data import global_statics as gs
# from main.data import dialogue_statics as ds

class BaseButton():
    def __init__(self, r, info_dict, activate=True, enable = True):
        self.x = info_dict["x"]
        self.y = info_dict["y"]
        self.width = info_dict["width"]
        self.height = info_dict["height"]
        self.text = info_dict["text"]
        self.wraplength = info_dict["wraplength"]
        self.button = Button(r,  
                             activebackground=gs.HOVER, 
                             activeforeground=gs.FG_COLOR,             
                             highlightbackground=gs.FG_COLOR,bg=gs.FG_COLOR, 
                             fg=gs.DARK_BG, 
                             text= self.text, 
                             wraplength=self.wraplength)

        # font = tkFont.Font(font=("Helvetica", 12, "bold"))
        # text_width = font.measure(self.text)
        # text_height = font.metrics("linespace")
        # self.width = text_width + 20  # Add padding
        # self.height = text_height + 10

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
        self.button.config(
            bg=gs.FG_COLOR,
            fg=gs.DARK_BG,
            activebackground=gs.HOVER,
            activeforeground=gs.FG_COLOR,
            highlightbackground=gs.FG_COLOR,
            relief="flat",
            borderwidth=1
        )
        self.button.place(x = 5000, y = self.y, width=self.width, height=self.height)
    
    def activate(self):
        # print(f"*** ARYA DEBUG LOG :: BaseButton: activate")
        self.button.config(
            bg=gs.FG_COLOR,
            fg=gs.DARK_BG,
            activebackground=gs.HOVER,
            activeforeground=gs.FG_COLOR,
            highlightbackground=gs.FG_COLOR,
            relief="flat",
            borderwidth=1
        )
        self.button.place(x = self.x, y = self.y, width=self.width, height=self.height)

    def set_text(self, text):
         self.button.config(text= text)
         self.text = text

class DialogueView():
    
    def __init__(self, frame,  dict_info, widgets) -> None:
        
        #box data
        self.frame = frame
        self.x = dict_info["x"]
        self.y = dict_info["y"]
        self.width = dict_info["width"]
        self.height = dict_info["height"]
        self.font =  dict_info["font"]
        self.fg = dict_info["text_color"]
        self.bg = dict_info["bg"]
        self.wraplength = dict_info["wraplength"]

        # There should be a better software solution for this,
        # but I dont have time to think about it.
        self.key = None
        self.next_key = None

        self.widgets = widgets
        
        # print(f"*** ARYA DEBUG LOG :: DialogueView: __init__: {dict_info['wraplength']}")
        self.dbox = Label(
            frame,
            font=self.font,
            bg=self.bg,
            fg=self.fg,  # Optional: match theme
            wraplength=self.wraplength,
            anchor="nw",
            justify="left"
        )

        self.dbox.place(x = self.x, y = self.y, width= self.width, height=self.height)
        
        # self.button_press = False
        # self.button_press_1 = False
        # self.button_press_2 = False
        self.sentence = ""
        
        self.button_press_name = None
        self.button_press_name_1 = None
        self.button_press_name_2 = None

        self.button_mode = 0 #0 to 2 for each button

        self.btn1 = BaseButton(self.frame, dict_info["btn1_info"], activate=False, enable= False)
        self.btn2 = BaseButton(self.frame, dict_info["btn2_info"], activate=False, enable= False)
        self.btn =  BaseButton(self.frame, dict_info["btn_info"], activate=False, enable=False)

        self.btn.add_event(self.button_press_event)
        self.btn1.add_event(self.button_press_event)
        self.btn2.add_event(self.button_press_event)


        self.display()
    
    def set_sentence(self, string):
        self.sentence = string

    def display(self):
        self.dbox.config(text = self.sentence)
        Tk.after(self.frame, 100, self.display)
    
    def set_key(self, key):
        self.key = key
        # self.next_key = nex_key
    
    # a lousy way to find out which button is pressed
    
    #btn 
    def button_press_event(self):
        # print(f"*** ARYA DEBUG LOG :: button pressed: {self.btn.text}")        # post event button press
        event_manager.EventManager.post_event("dialogue_answer", self.widgets)

        # there should be a better solution to this
        print(f"***ARYA DEBUG LOG :: the dialogue key is {self.key}")
        # if(self.key == "timer_1" or self.key not in ): 
        #     event_manager.EventManager.post_event("freeze_controls", False)

        # idk if this is setting it or just renaming it.
        # self.button_press_name = self.btn.text
        # not needed
        # self.d_view.hide_buttons(self.curr_avalogue[1].button_num)
        # self.curr_avalogue = None
        # self.btn_press_name = self.view.button_press_name

    #btn 1
    # def button_press_event_1(self):
    #     self.button_press_name_1 = self.btn1.text
    # #btn 2
    # def button_press_event_2(self):
    #     self.button_press_name_2 = self.btn2.text   
         
    def set_buttons(self,num, text = "", text1 = "", text2= ""):
        if num == 0:
              return
        elif num == 1:
            #   self.btn.activate()
              self.btn.set_text(text)
              self.btn.add_event(self.button_press_event)
              
        elif num == 2:
            #  self.btn1.activate()
             self.btn1.set_text(text1)
             self.btn1.add_event(self.button_press_event)

            #  self.btn2.activate()
             self.btn2.set_text(text2)
             self.btn2.add_event(self.button_press_event)

    # def hide_buttons(self, num):
    #     if num == 0:
    #         return
    #     elif num == 1:
    #         self.btn.deactivate()
              
    #     elif num == 2:
    #         self.btn1.deactivate()
    #         self.btn2.deactivate()
         
    def enable_buttons(self, num):
        if num == 0:
            return
        elif num == 1:
            self.btn.activate()
            self.btn.enable()
        elif num == 2:
            self.btn1.activate()
            self.btn1.enable()
            self.btn2.activate()
            self.btn2.enable()
    
    def disable_buttons(self, num):
        if num == 0:
              return
        elif num == 1:
              self.btn.disable()
        elif num == 2:
             self.btn1.disable()
             self.btn2.disable()

    def deactivate_buttons(self, num):
        if num == 0:
              return
        elif num == 1:
              self.btn.deactivate()
        elif num == 2:
             self.btn1.deactivate()
             self.btn2.deactivate()

class DialogueObject():
    
    def __init__(self, dict_info, widgets):
        

        self.key = dict_info["key"]
        self.button_num = int(dict_info["btn_num"])
        self.button_title = dict_info["btn_title"]
        self.button1_title = dict_info["btn1_title"]
        self.button2_title = dict_info["btn2_title"]   
        self.random = eval(dict_info["random"].lower().capitalize()) #choose text randomly from the list of texts or not
        self.sociality = dict_info["sociality"]
        self.next = dict_info["next"] #next dialogue key

        self.widgets = widgets

        if self.random:
            self.full_text = self.return_random_d(dict_info["text"])
        else: 
            self.full_text = str(dict_info["text"]) 
            
        self.str_index= 0
        self.shown_text = ""
        self.remaining_text = self.full_text
        
        # if this is true, the dialogue will wait for a button press
        self.forced_reply = eval(dict_info["forced_reply"].lower().capitalize())
       
        self.wipe_time = int(dict_info["wipe_time"])

        self.wait_before_start = int(dict_info["wait_before_start"])
        self.space_pause = 0.2
        self.letter_pause = 0.1
        
        # this is to retain the state of the dialogue
        # once we are going back to it after an interrupting dialogue.
        
        # state dict is from avalogue.py
        # setting to the starting state of a dialogue
        self.state = 0
        self.interrupted = False
        # if we repeat the itnerrupted dialogue, this will be true
        # so to avoid more repetitions
        self.repeated = False
        
        self.event = threading.Event()
        self.event.set()
      
    def return_random_d(self,string):
            list = string.split(",")

            if len(list) == 1:
                return list[0]
            else:
                rand = random.randint(0, len(list)-1)
                return list[rand]

    def update_texts(self, mystr):
        if mystr == "\\":
            mystr="\n"
        
        self.shown_text += mystr
        # print("*Shown Text*; " + self.shown_text)
        


    @utils.thread
    def letterbyletter(self):
        
        time.sleep(self.wait_before_start)

        if(self.sociality=='ns'):
            for l in self.full_text:
                self.event.wait()
                if l == " ":   
                    time.sleep(self.space_pause)
                else:
                    #playsound.playsound("/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/sounds/bleep_sliced.wav")
                    time.sleep(global_config.beep_sliced_sound.get_length() * 1.5)
                    global_config.beep_sliced_sound.play()

                self.update_texts(l)
        
        elif(self.sociality=='s'):
            # for every alternating word, play the sound
            alternate = 0
            for w in self.full_text.split():
                # print(w)
                alternate += 1
                               
                # word gap
                self.update_texts(w+' ')
                if alternate % 2 == 0:
                    continue
                self.event.wait()
                time.sleep(self.space_pause)
                sound = random.choice(global_config.animalese_sound)
                time.sleep(sound.get_length() - 2*self.space_pause)
                sound.play()
        else:
            pass # TODO should raise error
                
        event_manager.EventManager.post_event("dialogue_wait_response", self.widgets)
        # if we are telling it to wait for a button press
        # if not self.forced_reply: 
        #     self.wipe(self.wipe_time)
        
    def pause_letterbyletter(self, state):
        self.curr_avalogue[1].interrupted = True
        self.state = state
        self.event.clear()

    def start_letterbyletter(self):
        # print(f"*** ARYA DEBUG LOG :: DialogueObject: start_letterbyletter: want to see how many times this gets called")
        
        # means if it was interrupted before unpausing, or is this a new dialogue starting
        # if interrupted, how many times has it been interrupted, hence the use of repeated
        if self.interrupted and not self.repeated:
            self.repeated = True
            # add reciting text to the shown text


        self.letterbyletter()
        self.event.set()
       
    # @utils.thread
    # def wipe(self, wipe_time):
    #     time.sleep(wipe_time)
    #     self.shown_text = " "
    #     time.sleep(0.05)
    #     self.finished = True

class DialogueModel():
     def __init__(self, frame,  csv_filepath) -> None:
          self.frame = frame
          self.csv_filepath = csv_filepath
          self.dialogue_key = None

     def find_obj(self, key, avalogue):
          self.dialogue_key = key
        #   print(f"*** ARYA DEBUG LOG :: DialogueModel: find_obj: {key}")
          with open(self.csv_filepath, mode='r', newline='') as csv_f:
               csv_reader = csv.DictReader(csv_f, skipinitialspace=True)
               line_count = 0
               for row in csv_reader:
                        # print(f"*** ARYA DEBUG LOG :: DialogueModel: find_obj: {row}")
                        if row['key'] == key:
                             return DialogueObject(row, avalogue)

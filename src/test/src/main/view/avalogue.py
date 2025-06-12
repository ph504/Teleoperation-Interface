from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

import random
import time
import dialogue
import avatar_view
from main.control import event_manager
from collections import deque
from main.utils import utils
import tkinter as tk
from main.data import global_config as gc
from main.data import dialogue_statics as ds
state_dict = {
    # avatar is showing
    "showing": 0, 
    # avatar is finished showing and waiting for button, or is idle
    "wait_button": 1,
    # avatar is finshed
    "finished": 2,
}
class AvalogueController():
    def __init__(self, frame, 
                 d_model: dialogue.DialogueModel,
                 d_view: dialogue.DialogueView, 
                 a_model: avatar_view.AvatarModel, 
                 a_view: avatar_view.AvatarView):
        self.frame = frame 

        self.a_model = a_model
        self.a_view = a_view
        self.d_view = d_view
        self.d_model = d_model

        self.idle_for_seconds = 0
        self.is_event = False
        self.curr_avalogue = None #in form of a tuple?

        self.idle_avatar = self.a_model.find_obj('i_default')
        self.sad_idle_avatar = self.a_model.find_obj('i_sad')
        
        #a tuple = first var is avatar, second var is dialogue
        self.avalogue_stack = deque()

        # this is to control the flow of the avalogue in the update loop
        self.state = state_dict["finished"]
        self.interrupt_ongoing = False

        # EventManager.subscribe("congratulations", self.on_congrats)
        # EventManager.subscribe("mistake", self.on_mistake)
        self.update_loop()

    def btnpress_event(self):
        
        self.d_view.deactivate_buttons(self.curr_avalogue[1].button_num)
        # key gets updated when we search for the key in the model
        if self.curr_avalogue[1].next != None:
            self.set_avalogue("t_default", self.curr_avalogue[1].next)
        else:
            self.set_avalogue("i_default", self.curr_avalogue[1].key)
        # we reset the avalogue because it's going to be assigned with the avalogue stack, in the update loop
        self.curr_avalogue = None
        self.state = state_dict["finished"]
        # set the next dialogue and avatar depending on the next_key
        

        # tk.Tk.after(self.frame, 50, self.update_btnpress)

    #the avatar is dependent on the dialogue
    def update_loop(self):
        # print("*** ARYA DEBUG LOG :: --- UPDATE LOOP")
        # either no avalogue or the previous one is finished
        if self.state == state_dict["finished"]:   
            # no avalogue yet, change to idle      
            # print(f"*** ARYA DEBUG LOG :: --- a new avalogue is added to stack {self.avalogue_stack}")
            if not self.avalogue_stack:
                self.idle_view()

            # previous one is finished
            else:
                # print("*** ARYA DEBUG LOG :: --- a new avalogue is added to stack")
                self.start_dialogue()
                # print(f"*** ARYA DEBUG LOG :: --- a new avalogue is added to stack {self.curr_avalogue[1]}")
                self.state = state_dict["showing"]
                self.interrupt_ongoing = False
            
        else:
            self.update_view()
            # if there was an interrupt, 
            # we should call start letter by letter... 
            # but shouldnt do that if it was interrupted more than once
            if not self.interrupt_ongoing:
                self.polling_avalogue_stack()
                self.state = state_dict["showing"]
                self.interrupt_ongoing = True


        if self.state == state_dict["wait_button"]:
            # print("*** ARYA DEBUG LOG :: --- full text is shown and is either waiting for button or to wipe")
            # change the avatar to idle
            if self.curr_avalogue[0].type == "Talking":
                #print("11 --- for talking it needs to be idle(default/sad) while waiting for button, and wipe?")
                if self.curr_avalogue[0].emotion == "sad":
                    new_avalogue = (self.sad_idle_avatar, self.curr_avalogue[1])
                    self.curr_avalogue = new_avalogue
                else:
                    new_avalogue = (self.idle_avatar, self.curr_avalogue[1])
                    self.curr_avalogue = new_avalogue

            # enable the buttons to be pressed
            # print("*** ARYA DEBUG LOG :: --- waiting for buttons, enable it and if talking it should be idle")
            self.d_view.enable_buttons(self.curr_avalogue[1].button_num)

        # if not self.curr_avalogue[1].showing and not self.curr_avalogue[1].stopped:
        #     print(f"*** ARYA DEBUG LOG :: --- THIS HAPPENED waiting for start!!!!!!!!!")
        # #    print("5 --- it is waiting for start (in seconds)")
        #     self.empty_view()

        # elif self.curr_avalogue[1].showing and not self.curr_avalogue[1].stopped:
        #     #  print("6 --- it is talking")
        #         self.update_view()
        #         #if self.curr_avalogue[1].queue_flag and self.curr_avalogue[1].forced_reply:
        #         # print("7 --- if the avalogue that was showing, got hidden and now is showing again had buttons, enable it(should we?)")
        #         # self.d_view.enable_buttons(self.curr_avalogue[1].button_num)

        # elif not self.curr_avalogue[1].showing and self.curr_avalogue[1].stopped and not self.curr_avalogue[1].finished:
        #     # print("8 --- it is waiting for button")
        
            
                
                # if self.curr_avalogue[1].key == "choice_q":
                #     #print("!!! --- START COUNTDOWN")
                #     event_manager.EventManager.post_event("start_cntdwn", -1)

            

        tk.Tk.after(self.frame, 100, self.update_loop)
       
    
    def polling_avalogue_stack(self):
        # there is something in the stack and the current avalogue is not finished
        if self.avalogue_stack:
            # change state of dialogue
            # change state of avalogue
            self.curr_avalogue[1].pause_letterbyletter(self.state)
            temp = self.curr_avalogue
            self.start_dialogue()
            self.avalogue_stack.append(temp)
            
    def wait_for_button(self):
        self.state = state_dict["wait_button"]

    def start_dialogue(self):
        self.curr_avalogue = self.avalogue_stack.pop()
        self.curr_avalogue[1].start_letterbyletter()
        if self.curr_avalogue[1].button_num != 0:
            # print("4 --- if the previous avalogue had buttons, disable it")
            self.d_view.disable_buttons(self.curr_avalogue[1].button_num)

    def update_view(self):
        self.d_view.set_sentence(self.curr_avalogue[1].shown_text)
        img = self.curr_avalogue[0].get_currimage()
        self.a_view.set_image(img)

    def idle_view(self):
        self.d_view.set_sentence('')
        img = self.idle_avatar.get_currimage()
        self.a_view.set_image(img)

    def set_controls(self, d_key):
        # print(f"*** ARYA DEBUG LOG :: --- set_controls {d_key}")
        # this is to set the controls for the dialogue
        if d_key in ds.DISABLE_CONTROL_DIALOGUE_KEYS:
            # print(f"*** ARYA DEBUG LOG :: --- enable controls {d_key}")
            event_manager.EventManager.post_event("freeze_controls", True)
            # timer pause
        elif d_key in ds.ALL_DIALOGUE_KEYS:
            event_manager.EventManager.post_event("freeze_controls", False)
            # timer resume or start
        else:
            raise ValueError(f"The key {d_key} is not in the list of dialogue keys {ds.ALL_DIALOGUE_KEYS}")

    def set_avalogue(self, a_key, d_key):
        # print(f"*** ARYA DEBUG LOG :: --- set_avalogue {d_key}")
        # there should be a better solution
        # self.d_view.set_key(d_key)
        self.set_controls(d_key)

        avatar_obj  = self.a_model.find_obj(a_key)
        
        dialogue_obj = self.d_model.find_obj(d_key, self)
        
        self.d_view.set_buttons(dialogue_obj.button_num, 
                                dialogue_obj.button_title,
                                dialogue_obj.button1_title,
                                dialogue_obj.button2_title)
        
        self.avalogue_stack.append((avatar_obj, dialogue_obj))
   

    def on_congrats(self, dummy):
        self.set_avalogue("r_happy", "congrats")
    
    def on_collision(self, dummy):
        # disable controls because we want the controls to freeze if we have collision, to grab extra attention
        # event_manager.EventManager.post_event("enable_controls", False)
        d_key = random.choice(ds.COLLISION_DIALOGUE_KEYS)
        self.set_avalogue("r_sad",d_key)
        # play error sound depending on the sociality
        sound = gc.get_collision_sound()
        sound.play()
        time.sleep(1.5)

        
        

        
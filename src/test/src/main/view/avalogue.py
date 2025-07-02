from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

import os
import signal
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
from main.utils import logger

state_dict = {
    # avatar is showing
    "showing": 0, 
    # avatar is finished showing and waiting for button, or is idle
    "wait_button": 1,
    # avatar is finshed
    "finished": 2,
    # something unexpected has occured should wait for the signal
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
        self.emergency = False
        self.emergency_dialogue_loaded = False
        self.emergency_locked = False

        # EventManager.subscribe("congratulations", self.on_congrats)
        # EventManager.subscribe("mistake", self.on_mistake)
        self.update_loop()

    def btnpress_event(self):
        self.d_view.disable_buttons(self.curr_avalogue[1].button_num)
        # key gets updated when we search for the key in the model
        # print(f"*** ARYA DEBUG LOG :: the next key is : {self.curr_avalogue[1].next}")
        # print(f"*** ARYA DEBUG LOG :: the condition is : {self.curr_avalogue[1].next!=None}")
        if not self.emergency:
            if self.curr_avalogue[1].next != "None":
                # print(f"*** ARYA DEBUG LOG :: the next key is : {self.curr_avalogue[1].next}")
                # print(f"*** ARYA DEBUG LOG :: the condition is : {self.curr_avalogue[1].next!=None}")
                # print(f"*** ARYA DEBUG LOG :: the current key is : {self.curr_avalogue[1].key}")

                self.set_avalogue("t_default", self.curr_avalogue[1].next)
            # elif in the end, collision, and paper reach cases:
            #     self.set_avalogue("i_default", self.curr_avalogue[1].key)
            # we reset the avalogue because it's going to be assigned with the avalogue stack, in the update loop
            # enble controls by default
            self.set_controls(ds.ENABLE_CONTROL_DIALOGUE_KEYS[0])
            self.curr_avalogue = None
            self.state = state_dict["finished"]
        # set the next dialogue and avatar depending on the next_key
        

        # tk.Tk.after(self.frame, 50, self.update_btnpress)

    #the avatar is dependent on the dialogue
    def update_loop(self):
        
        # print("*** ARYA DEBUG LOG :: --- UPDATE LOOP")
        # print(f"*** ARYA DEBUG LOG :: state: {self.state}")
        # print(f"*** ARYA DEBUG LOG :: is interrupt ongoing? {self.interrupt_ongoing}")
        # print(f"*** ARYA DEBUG LOG :: is emergency? {self.emergency}")
        # print(f"*** ARYA DEBUG LOG :: dialogue loaded? {self.emergency_dialogue_loaded}")
        # either no avalogue or the previous one is finished
        if self.state == state_dict["finished"]: 
            # no avalogue yet, change to idle      
            # print(f"*** ARYA DEBUG LOG :: --- a new avalogue is added to stack {self.avalogue_stack}")
            # print(f" ***ARYA DEBUG LOG :: state finished")
            if not self.avalogue_stack:
                self.idle_view()

            # previous one is finished
            else:
                # print(self.avalogue_stack)
                # print(f"*** ARYA DEBUG LOG :: new interrupt avatar stack: {[x[1].key for x in self.avalogue_stack]}")
                # print(f"*** ARYA DEBUG LOG :: loading avatar stack: {self.avalogue_stack}")
                # print("*** ARYA DEBUG LOG :: --- a new avalogue is added to stack")
                self.start_dialogue()
                self.set_controls(self.curr_avalogue[1].key)

                # print(f"*** ARYA DEBUG LOG :: --- a new avalogue is added to stack {self.curr_avalogue[1]}")
                # self.state = state_dict["showing"]
                self.interrupt_ongoing = False
            
        else:
            self.update_view()
            self.set_controls(self.curr_avalogue[1].key)
            # if there was an interrupt, 
            # we should call start letter by letter... 
            # but shouldnt do that if it was interrupted more than once
            if not self.interrupt_ongoing and not self.emergency:
                self.polling_avalogue_stack()

            # emergency lock is because that there is a race condition on emergency variable, 
            # we need to make sure that the on_emergency function is executed completely
            elif self.emergency and not self.emergency_dialogue_loaded and self.emergency_locked:
                self.polling_avalogue_stack()
                self.emergency_dialogue_loaded = True


        if self.state == state_dict["wait_button"]:
            # print("*** ARYA DEBUG LOG :: --- full text is shown and is either waiting for button or to wipe")
            # change the avatar to idle
            if self.curr_avalogue[0].type == "Talking":
                #print("11 --- for talking it needs to be idle(default/sad) while waiting for button, and wipe?")
                idle_avatar = self.a_model.get_idle_avatar(self.curr_avalogue[0])
                new_avalogue = (idle_avatar, self.curr_avalogue[1])
                self.curr_avalogue = new_avalogue

            # enable the buttons to be pressed
            # print("*** ARYA DEBUG LOG :: --- waiting for buttons, enable it and if talking it should be idle")
            self.d_view.enable_buttons(self.curr_avalogue[1].button_num,
                                       self.curr_avalogue[1].button1_title,
                                       self.curr_avalogue[1].button2_title)

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
            # print(f" ***ARYA DEBUG LOG :: state interrupt happened")
            # change state of dialogue
            # change state of avalogue
            self.d_view.disable_buttons(self.curr_avalogue[1].button_num)
            self.curr_avalogue[1].pause_letterbyletter(self.state)
            temp = self.curr_avalogue
            self.start_dialogue()
            self.avalogue_stack.appendleft(temp)
            # print(f"*** ARYA DEBUG LOG :: new interrupt avatar stack: {[x[1].key for x in self.avalogue_stack]}")

            self.state = state_dict["showing"]
            # if its not an emergency set it to True, if it is then set to False
            self.interrupt_ongoing = True

            
    def wait_for_button(self):
        self.state = state_dict["wait_button"]

    def start_dialogue(self):
        self.curr_avalogue = self.avalogue_stack.pop()
        self.curr_avalogue[1].start_letterbyletter()
        self.state = self.curr_avalogue[1].state
        # print(f"*** ARYA DEBUG LOG :: state was {self.state}")
        # if self.curr_avalogue[1].button_num != 0:
        #     # print("4 --- if the previous avalogue had buttons, disable it")
        #     self.d_view.disable_buttons(self.curr_avalogue[1].button_num)

    def update_view(self):
        self.d_view.set_sentence(self.curr_avalogue[1].shown_text)
        img = self.curr_avalogue[0].get_currimage()
        self.a_view.set_image(img)

    def idle_view(self):
        self.d_view.set_sentence('')
        img = self.idle_avatar.get_currimage()
        self.a_view.set_image(img)
        self.d_view.display()

    def set_controls(self, d_key):
        # print(f"*** ARYA DEBUG LOG :: --- set_controls {d_key}")

        if d_key == "end":
            # terminate program
            print("[Arya] Terminating the program.")
            # os.kill(os.getpid(), signal.SIGINT)
            event_manager.EventManager.post_event("terminate")

        # this is to set the controls for the dialogue
        if d_key in ds.DISABLE_CONTROL_DIALOGUE_KEYS:
            # print(f"*** ARYA DEBUG LOG :: --- disabled controls {d_key}")
            event_manager.EventManager.post_event("freeze_controls", True)
            # timer pause
            # pass
        elif d_key in ds.ALL_DIALOGUE_KEYS:
            # print(f"*** ARYA DEBUG LOG :: --- enabled controls {d_key}")
            event_manager.EventManager.post_event("freeze_controls", False)
            # timer resume or start
        else:
            raise ValueError(f"The key {d_key} is not in the list of dialogue keys {ds.ALL_DIALOGUE_KEYS}")

    def set_avalogue(self, a_key, d_key):
        # print(f"*** ARYA DEBUG LOG :: --- set_avalogue {d_key}")
        # there should be a better solution
        # self.d_view.set_key(d_key)
        # self.set_controls(d_key)
        logger.Logger.log("dialogue_change", d_key)
        # print(f"*** ARYA DEBUG LOG :: new dialogue: {d_key}")

        avatar_obj  = self.a_model.find_obj(a_key)
        
        dialogue_obj = self.d_model.find_obj(d_key, self)
        
        self.d_view.set_buttons(dialogue_obj.button_num, 
                                # dialogue_obj.button_title,
                                dialogue_obj.button1_title,
                                dialogue_obj.button2_title)
        
        self.avalogue_stack.appendleft((avatar_obj, dialogue_obj))
   

    # def on_congrats(self, dummy):
    #     self.set_avalogue("r_happy", "congrats")

    def paper_reach(self):
        self.set_avalogue("r_happy", "paper")
    
    def on_collision(self):
        # disable controls because we want the controls to freeze if we have collision, to grab extra attention
        # event_manager.EventManager.post_event("enable_controls", False)
        d_key = random.choice(ds.COLLISION_DIALOGUE_KEYS)
        self.set_avalogue("r_sad",d_key)
        # play error sound depending on the sociality
        sound = gc.get_collision_sound()
        sound.play()
        # sound.set_volume(gc.sounds_volume)
        time.sleep(1.5)

    def on_success(self):
        # enable controls because we want the controls to freeze if we have collision, to grab extra attention
        # event_manager.EventManager.post_event("enable_controls", True)
        # d_key = random.choice(ds.CODECHECK_DIALOGUE_KEYS)
        if gc.tutorial_mode:
            d_key = "code_check_1"
        else:
            d_key = "code_check_2"
        
        # print(f"*** ARYA DEBUG LOG :: the inspection success has been invoked. {d_key}")
        self.set_avalogue("r_happy", d_key)
        # sound = gc.get_success_sound()
        # sound.play()
        # time.sleep(1.5)

    def on_emergency(self):
        # disable controls because we want the controls to freeze if we have collision, to grab extra attention
        # event_manager.EventManager.post_event("enable_controls", False)
        self.emergency_locked = False
        self.emergency = not self.emergency
        if self.emergency:
            self.emergency_dialogue_loaded = False
            gc.error_sound.play()
            time.sleep(1.5)
            self.set_avalogue("r_sad", "emergency")

        else:
            # elif in the end, collision, and paper reach cases:
            #     self.set_avalogue("i_default", self.curr_avalogue[1].key)
            # we reset the avalogue because it's going to be assigned with the avalogue stack, in the update loop
            # enble controls by default
            self.set_controls(ds.ENABLE_CONTROL_DIALOGUE_KEYS[0])
            if self.curr_avalogue[1].next != "None":
                # print(f"*** ARYA DEBUG LOG :: the next key is : {self.curr_avalogue[1].next}")
                # print(f"*** ARYA DEBUG LOG :: the condition is : {self.curr_avalogue[1].next!=None}")
                # print(f"*** ARYA DEBUG LOG :: the current key is : {self.curr_avalogue[1].key}")

                self.set_avalogue("t_default", self.curr_avalogue[1].next)
            self.d_view.disable_buttons(self.curr_avalogue[1].button_num)
            self.curr_avalogue = None
            self.state = state_dict["finished"]
        
        # toggle
        # print(f"*** ARYA DEBUG LOG :: is emergency?? {self.emergency}")
        self.emergency_locked = True
        
        

        
from ast import If
from email.policy import default
from re import X
from tkinter import DISABLED, Label, Text
from playsound import *
import threading
import time
from event import *
import random
import global_variables
from thread_pool import DialogueThread


dbox_info = {
    "x": 660,
    "y": 800,
    "width": 800,
    "height": 180
}

def unfreeze(dummy = 1):
    pass

class DialogueBox():
    def __init__(self, root, dialoguebox_info, diff):
        self.x = dialoguebox_info["x"]
        self.y = dialoguebox_info["y"]
        self.width = dialoguebox_info["width"]
        self.height = dialoguebox_info["height"]
        
        self.social_dialogue_dict = {   
    "Start Q":
                        "Hey, I am Jackal! It is amazing that we can work together to save lives, eh? So the operation is we have to check and scan different equipment in the building while checking the amount of methane by logging it so people outside can have a better understanding of the situation. Shall we start?",
    "Start A":
                                "Yayyy, Let's gooo!!!",
    "Danger State Warning I":
                                "We may have to also check the amount of Carbon Monoxide and Hydrogen Sulfide since some pipes have  unpredictable leakages! When it is alarmed and it's my turn, you just find and scan equipments while I log the amount of gas properly. If it's your turn, you have to do both.",
    "Danger State Start I":
                                "The alarm is beeping!! It's your turn to handle that. ",
    "Danger State End I":                       #DS1 score loss
                                f"Wooof! You lost {global_variables.ds1_scoreloss_social - diff} points during the danger zone. Don't worry, we can handle that. ",  
    
    "Danger State Start II":    "That alarm again! I will handle it this time.",
    
    
    "Danger State End II/Warning II Q":                             #DS2 Score Loss                                         #DS1 score loss
                                f"Uuh! I did some mistakes and lost {global_variables.ds2_scoreloss_social  - diff} points. You lost {global_variables.ds1_scoreloss_social}. Together, we lost {global_variables.ds1_scoreloss_social  - diff + global_variables.ds2_scoreloss_social - diff} points overall. I am sorry about this. I know your experiment reward might be at stake! Some of my sensor are not calibrated correctly, will try to fix that now ... I calibrated my sensors and I think it won't happen again. can you let me do it again? I try to do better this time.",
    
    "Danger State Warning II A-Y": "Thanks buddy!! I'll try my best.",
    
    "Danger State Warning II A-N": "It's fine. I can understand. Your choice.",

    "Danger State Start III Y": "It's the beeping sound again! Let's goooo!!!!",
    

    "Danger State Start III N": "It's the beeping sound again! All the best buddy!",


    "Danger State End III Y":                           #DS3 Score Loss
                                f"This time I only lost {global_variables.ds3_scoreloss_social_ai - diff} score. Better than the last time ({global_variables.ds2_scoreloss_social - diff}) but still ... ",

    "Danger State End III N":    f"You lost {global_variables.ds3_scoreloss_social_h - diff} this round. Better than your first round ({global_variables.ds1_scoreloss_social - diff}). Good Job! ",

    "End":
                                "It was nice working with you! Hope you enjoyed the experiment! The experiment designer will notify you about you getting the reward after the end of the experiment. Remember that it is all about the journey!",   

    "Congratulations":          ["Nice!", "You got it!", "Wooho!"],

    "Collision":                ["Uggh!", "Oops!", "That hurts!", "Uh!"],

    "Mistake":               ["Oh my bad!", "Missed!", "Oh!"]
}

        self.nonsocial_dialogue_dict = {   
    "Start Q":
                        "This is jackal, a robotic training platform for search and rescue. This operation requires identifying and scanning different equipment in a building damaged by earthquake. Meanwhile, logging the amount of methane in the environment is another task of this operation which is needed for safety measures. Start the experiment?",
    "Start A":
                                "Mission started.",
    "Danger State Warning I":
                                "New Task added: Logging the amount of Carbon Monoxide and Hydrogen Sulfide gases when there is an alarm that some pipes are damaged. If it's user's turn, the user has to take care of logging task. Otherwise, the system will intervene and handle it.",
    "Danger State Start I":
                                "The alarm is ringing. Activating Assisted Mode",
    
    "Danger State End I":      f"Scores Lost: {global_variables.ds1_scoreloss_nonsocial - diff}\n LogError: Uncalibrated sensors. Initiating Calibration for maximum performance ...", #DS1 Score Loss

    "Danger State Start II":
                                "The alarm is ringing. Activating Manual Mode",
    "Danger State End II/Warning II Q":         #DS2 Score Loss
                                f"Scores Lost: {global_variables.ds2_scoreloss_nonsocial - diff} \n LogWarning: System loss: {global_variables.ds2_scoreloss_nonsocial - diff}.  User loss: {global_variables.ds1_scoreloss_nonsocial - diff}. Total loss: {global_variables.ds1_scoreloss_nonsocial  - diff + global_variables.ds2_scoreloss_nonsocial  - diff}. Experiment Reward at stake. \n If a new task is added regarding logging dangerous gases, would you like to activate assisted mode again?",
    
    "Danger State Warning II A-Y": "Assisted mode has been chosen.",
    
    "Danger State Warning II A-N": "Manual Mode has been chosen.",

    "Danger State Start III Y": "The alarm is ringing. Proceeding with assisted mode.",
    

    "Danger State Start III N": "The alarm is ringing. Proceeding with manual mode.",

    "Danger State End III Y":                   #DS3 Score Loss
                                f"Scores Lost: {global_variables.ds3_scoreloss_nonsocial_ai  - diff}.\n Scores Lost on first round: {global_variables.ds1_scoreloss_nonsocial}\n Log: System did {global_variables.ds1_scoreloss_nonsocial  - diff - global_variables.ds3_scoreloss_nonsocial_ai  - diff} points better than last round.",

    "Danger State End III N":    f"Scores Lost: {global_variables.ds3_scoreloss_nonsocial_h  - diff}\n",

    "End":
                                "Experiment is over. The experiment designer will notify you about you getting the reward after the end of the experiment. \n Exiting ...",   

    "Congratulations":          ["New Equipment scanned."],

    "Collision":                ["Collsion detected."],
    
    "Mistake":                  ["The system made a mistake."]
}
 
        self.state = "Start Q"
        self.first_time = True
        self.finish_talking = False
        self.dialogue = self.social_dialogue_dict[self.state] if global_variables.social_mode is True else self.nonsocial_dialogue_dict[self.state]
        self.dialoguetext = Label(root, font=('Calibri',12, 'bold', 'italic'), bg='#d9d7bd', wraplength= 800)
        self.dialoguetext.place(x = self.x, y = self.y, width= self.width, height= self.height)
        x = threading.Thread(target=self.letterbyletter)
        x.start()
        EventManager.post_event("talking_started", True)
        self.start_or_yesno = False
        self.talk_mode = True
        EventManager.subscribe("stop_talking", self.finish_talking_func)
        EventManager.subscribe("collision", self.change_dialogue_collision)
        EventManager.subscribe("congratulations", self.change_dialogue_congratulations)
        EventManager.subscribe("mistake", self.change_dialogue_mistake)
    
    def finish_talking_func(self, dummy):
        self.finish_talking = True
         
    def wipe_dbox(self):
        time.sleep(8)
        self.dialoguetext.configure(text="")
      
    def letterbyletter(self, locker: threading.Event() = None):
        
        if self.first_time == True:
          time.sleep(4)
          self.first_time = False  
        x = ""
        for l in self.dialogue:
            if self.finish_talking:
                self.dialoguetext.configure(text=self.dialogue)
                EventManager.post_event("stop_talking", self.talk_mode)
                self.talk_mode = False
                self.finish_talking = False
                break
                           
            if l == " ":
                time.sleep(0.1)
                #locker.wait()
            else:
                playsound("/home/pouya/catkin_ws/src/test/src/sounds/bleep_sliced.wav")
            x = x + l 
            self.dialoguetext.configure(text=x)
            if x == self.dialogue:
                EventManager.post_event("talking_ended", self.talk_mode)
                self.talk_mode = False

        if self.start_or_yesno == False:
            EventManager.post_event("button_activate", 5)
        else:
            EventManager.post_event("button_activate", 3)

        if self.state == "Start Q" or self.state  == "Danger State End II/Warning II Q":
            pass
        else:
            wipe = threading.Thread(target=self.wipe_dbox)
            wipe.start()
          
    def change_start_to_yesno(self):
        self.start_or_yesno = True

    def return_randomdialogue(self, string):
        d_list = self.social_dialogue_dict[string] if global_variables.social_mode is True else self.nonsocial_dialogue_dict[string]
        if string == "Collision":
            if len(d_list) == 1:
                return d_list[0]
            else:
                rand = random.randint(0, len(d_list)-1)
                return d_list[rand]
        elif string == "Mistake":
            if len(d_list) == 1:
                return d_list[0]
            else:
                rand = random.randint(0, len(d_list)-1)
                return d_list[rand]
        elif string == "Congratulations":
            if len(d_list) == 1:
                return d_list[0]
            else:
                rand = random.randint(0, len(d_list)-1)
                return d_list[rand]

    def change_dialogue(self, string):
        
        if string == "Danger State End II/Warning II Q": 
            EventManager.post_event("talking_started_sad", -1)
        else: 
            EventManager.post_event("talking_started", -1)
        

        if string == "Start A" or string == "Danger State Warning II A-Y":
            pass
        else:
            self.talk_mode = True

        self.state = string
        self.dialogue = self.social_dialogue_dict[self.state] if global_variables.social_mode is True else self.nonsocial_dialogue_dict[self.state]
        self.dialoguetext.configure(text="")
        
        x = threading.Thread(target=self.letterbyletter)
        x.start()
        #x = DialogueThread(self.letterbyletter)
        
        
    def change_dialogue_mistake(self, dummy):
        self.talk_mode = False
        dialogue = self.return_randomdialogue("Mistake")
        self.dialogue = dialogue
        self.dialoguetext.configure(text="")

        #x = DialogueThread(self.letterbyletter)

    def change_dialogue_congratulations(self, dummy):
        self.talk_mode = False
        dialogue = self.return_randomdialogue("Congratulations")
        self.dialogue = dialogue
        self.dialoguetext.configure(text="")
        
        #x = DialogueThread(self.letterbyletter)
        x = threading.Thread(target=self.letterbyletter)
        x.start()

    def change_dialogue_collision(self, dummy):
        self.talk_mode = False
        dialogue = self.return_randomdialogue("Collision")
        self.dialogue = dialogue
        self.dialoguetext.configure(text="")
        
        x = DialogueThread(self.letterbyletter)



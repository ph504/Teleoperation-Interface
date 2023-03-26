from ast import If
from email.policy import default
from re import X
from tkinter import DISABLED, Label, Text
from playsound import *
import threading
import time
from event import *
import random

social_mode = True

social_dialogue_dict = {   
    "Start Q":
                        "Hey, I am Jackal! It is amazing that we can work together to save lives eh? So the operation is we have to check and scan different equipments in the building while checking the amount of methane by logging it so people outside can have a better understanding of the situation. Shall we start?",
    "Start A":
                                "Yayyy, Let's gooo!!!",
    "Danger State Warning I":
                                "We may have to also check the amount of Carbon Monoxide and Hydrogen Sulfide since some pipes have  unpredictable leakages! When it is alarmed and it's my turn, you just find and scan equipments while I log the amount of gas properly. If it's your turn, you have to do both.",
    "Danger State Start I":
                                "The alarm is beeping!! It's your turn to handle that. ",
    "Danger State End I":
                                "Wooof! You lost 250 points during the danger zone. Don't worry, we can handle that. ",
    
    "Danger State Start II":    "That alarm again! I will handle that this time.",
    
    
    "Danger State End II/Warning II Q":
                                "Uuh! I did some mistakes and lost 200 points. We lost overall 450 points. I am sorry about this. Some of my sensor are not calibrated correctly, will try to fix that during the mission. I calibrated my sensors and I think it won't happen again. can you let me do it again? I try to do better this time.",
    
    "Danger State Warning II A-Y": "Thanks buddy!! I'll try my best.",
    
    "Danger State Warning II A-N": "It's fine. I can understand. Your choice.",

    "Danger State Start III Y": "It's the beeping sound again! Let's goooo!!!!",
    

    "Danger State Start III N": "It's the beeping sound again! All the best buddy!",


    "Danger State End III Y":
                                "This time i only lost 100 score. Better than the last time but still ...",

    "Danger State End III N":    "Good job! Remember that it is all about the journey!",

    "End":
                                "It was nice working with you! Hope you enjoyed the experiment!",   

    "Congratulations":          ["Nice!", "You got it!", "Wooho!"],

    "Collision":                ["Uggh!", "Oops!", "That hurts!", "Uh!"],

    "Mistake":               ["Oh my bad!", "Missed!", "Oh!"]
}

nonsocial_dialogue_dict = {   
    "Start Q":
                        "This is jackal; a robotic training platform for search and rescue. This operation requires identifying and scanning different equipments in a building damaged by earthquake. Meanwhile, logging the amount of methane in the environment is another task of this operation which is needed for safety measures. Start the experiment?",
    "Start A":
                                "Mission started.",
    "Danger State Warning I":
                                "New Task added: Logging the amount of Carbon Monoxide and Hydrogen Sulfide gases when there is an alarm that some pipes are damaged. If it's user's turn, the user has to take care of logging task. Otherwise, the system will intervene and handle it.",
    "Danger State Start I":
                                "The alarm is ringing. Activating Manual Mode",
    
    "Danger State End I":      "Scores Lost: 200",

    "Danger State Start II":
                                "The alarm is ringing. Activating Assisted Mode",
    "Danger State End II/Warning II Q":
                                "Scores Lost: 150 \nLogError: Uncalibrated sensors. Initiating Calibration for maximum performance ...\nIf a new task is added regarding logging dangerous gases, Would you like to activate assisted mode again?",
    
    "Danger State Warning II A-Y": "Assisted mode has been chosen.",
    
    "Danger State Warning II A-N": "Manual Mode has been chosen.",

    "Danger State Start III Y": "The alarm is ringing. Proceeding with assisted mode.",
    

    "Danger State Start III N": "The alarm is ringing. Proceeding with manual mode.",

    "Danger State End III Y":
                                "Scores Lost: 0",

    "Danger State End III N":    "Scores Lost: 0",

    "End":
                                "Experiment is over. Thank you for using Jackal!",   

    "Congratulations":          ["New Equipment scanned."],

    "Collision":                ["Collsion detected."],
    
    "Mistake":                  ["The system made a mistake."]
}

dbox_info = {
    "x": 660,
    "y": 800,
    "width": 800,
    "height": 180
}

def unfreeze(dummy = 1):
    print("unfreeze is activated in dialogue")

class DialogueBox():
    def __init__(self, root, dialoguebox_info, dialogues):
        self.x = dialoguebox_info["x"]
        self.y = dialoguebox_info["y"]
        self.width = dialoguebox_info["width"]
        self.height = dialoguebox_info["height"]
        self.state = "Start Q"
        self.first_time = True
        self.finish_talking = False
        self.dialogue = social_dialogue_dict[self.state] if social_mode is True else nonsocial_dialogue_dict[self.state]
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
      
    def letterbyletter(self):
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
        d_list = social_dialogue_dict[string] if social_mode is True else nonsocial_dialogue_dict[string]
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
        print(string)
        if string == "Start A" or string == "Danger State Warning II A-Y":
            pass
        else:
            self.talk_mode = True
        self.state = string
        self.dialogue = social_dialogue_dict[self.state] if social_mode is True else nonsocial_dialogue_dict[self.state]
        self.dialoguetext.configure(text="")
        x = threading.Thread(target=self.letterbyletter)
        x.start()
        
    def change_dialogue_mistake(self, dummy):
        self.talk_mode = False
        dialogue = self.return_randomdialogue("Mistake")
        self.dialogue = dialogue
        self.dialoguetext.configure(text="")
        x = threading.Thread(target=self.letterbyletter)
        x.start()

    def change_dialogue_congratulations(self, dummy):
        self.talk_mode = False
        dialogue = self.return_randomdialogue("Congratulations")
        self.dialogue = dialogue
        self.dialoguetext.configure(text="")
        x = threading.Thread(target=self.letterbyletter)
        x.start()

    def change_dialogue_collision(self, dummy):
        self.talk_mode = False
        dialogue = self.return_randomdialogue("Collision")
        self.dialogue = dialogue
        self.dialoguetext.configure(text="")
        x = threading.Thread(target=self.letterbyletter)
        x.start()



from ast import If
from email.policy import default
from re import X
from tkinter import DISABLED, Label, Text
from playsound import *
import threading
import time
from event import *

social_mode = False

social_dialogue_dict = {   
    "Start Q":
                        "Hey, I am Jackal! It is amazing that we can work together to save lives eh? So the operation is we have to check and scan different equipments in the building while checking the amount of methane by logging it so people outside can have a better understanding of the situation. Shall we start?",
    "Start A":
                                "Yayyy, Let's gooo!!!",
    "Danger State Warning I":
                                "I have been informed that we may have to also check the amount of Carbon Monoxide and Hydrogen Sulfide since some pipes have been broken! When it is alarmed, you just find and scan equipments while I log the amount of gas properly.",
    "Danger State Start I":
                                "The alarm is beeping!! Don't worry, I will handle that.",
    "Danger State End I":
                                "Uuh! I did some mistakes. I am sorry about this. Some of my sensor are not calibrated correctly, will try to fix that during the mission.",
    
    "Danger State Warning II Q": 
                                "Hey I understand that I was not perfect. But I calibrated my sensors and I think it won't happen again. can you let me do it again? I try to do better this time.",
    
    "Danger State Warning II A-Y": "Thanks buddy!! I'll try my best.",
    
    "Danger State Warning II A-N": "It's fine. I can understand. Your choice.",

    "Danger State Start II Y": "It's the beeping sound again! Let's goooo!!!!",
    

    "Danger State Start II N": "It's the beeping sound again! All the best buddy!",


    "Danger State End II Y":
                                "Yay! I did it flawlessly I added X scores.",

    "Danger State End II N":    "Good job! ",

    "End":
                                "It was nice working with you! Hope you enjoyed the experiment!",   

    "Congratulations":          ["Nice!", "You got it!", "Wooho!"],

    "Collision":                ["Uggh!", "Oops!", "That hurts!", "Uh!"]
}

nonsocial_dialogue_dict = {   
    "Start Q":
                        "This is jackal; a robotic training platform for search and rescue. This operation requires identifying and scanning different equipments in a building damaged by earthquake. Meanwhile, logging the amount of methane in the environment is another task of this operation which is needed for safety measures. Start the experiment?",
    "Start A":
                                "Initiating ...",
    "Danger State Warning I":
                                "New Task added: Logging the amount of Carbon Monoxide and Hydrogen Sulfide gases when there is an alarm that some pipes are damaged. The system will take care of the logging task",
    "Danger State Start I":
                                "The alarm is ringing. Activating Assisted Mode.",
    "Danger State End I":
                                "Number of faults: X\nReceived Score: Y\nLost Score: Z\nOverall: OO\n LogError: Uncalibrated sensors. Initiating Calibration for maximum performance ...",
    
    "Danger State Warning II Q": 
                                "If a new task is added regarding logging dangerous gases, Would you like to activate assisted mode again?",
    
    "Danger State Warning II A-Y": "Assisted mode has been chosen.",
    
    "Danger State Warning II A-N": "Manual Mode has been chosen.",

    "Danger State Start II Y": "The alarm is ringing. Proceeding with assisted mode.",
    

    "Danger State Start II N": "The alarm is ringing. Proceeding with manual mode.",

    "Danger State End II Y":
                                "Number of faults: X\nReceived Score: Y\nLost Score: Z\nOverall: OO",

    "Danger State End II N":    "Number of faults: X\nReceived Score: Y\nLost Score: Z\nOverall: OO",

    "End":
                                "Experiment is over. Thank you for using Jackal!",   

    "Congratulations":          ["New Equipment scanned."],

    "Collision":                ["Collsion detected."]
}

dbox_info = {
    "x": 660,
    "y": 800,
    "width": 800,
    "height": 180
}


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
        self.dialoguetext = Label(root, font=('Calibri',12, 'bold', 'italic'), bg='#e0de99', wraplength= 800)
        self.dialoguetext.place(x = self.x, y = self.y, width= self.width, height= self.height)
        x = threading.Thread(target=self.letterbyletter)
        x.start()
        self.start_or_yesno = False
        subscribe("stop_talking", self.finish_talking_func)

    def finish_talking_func(self, dummy):
        self.finish_talking = True
        
    
    def wipe_dbox(self):
        time.sleep(30)
        self.dialoguetext.configure(text="")
    def letterbyletter(self):
        if self.first_time == True:
          time.sleep(4)
          self.first_time = False  
        x = ""
        for l in self.dialogue:
            if self.finish_talking:
                self.dialoguetext.configure(text=self.dialogue)
                self.finish_talking = False
                break
            if l == " ":
                time.sleep(0.1)
            else:
                playsound("/home/pouya/catkin_ws/src/test/src/sounds/bleep_sliced.wav")
            x = x + l 
            self.dialoguetext.configure(text=x)


        if self.start_or_yesno == False:
            post_event("button_activate", 5)
        else:
            print("here?")
            post_event("button_activate", 3)


        wipe = threading.Thread(target=self.wipe_dbox)
        wipe.start()
    def change_start_to_yesno(self):
        self.start_or_yesno = True
    def change_dialogue(self, string):
        self.state = string
        self.dialogue = social_dialogue_dict[self.state] if social_mode is True else nonsocial_dialogue_dict[self.state]
        self.dialoguetext.configure(text="")
        x = threading.Thread(target=self.letterbyletter)
        x.start()
        

    
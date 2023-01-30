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
                                "Let's gooo!!!",
    "Danger State Start I":
                                "I have been informed that we have to also check the amount of Carbon Monoxide and Hydrogen Sulfide since some pipes have been broken! Beware since it is important if we do our jobs correctly here. Right now you just find and log injured people while I log the amount of gas properly.",
    "Danger State End I":
                                "Uuh! I did some mistakes. I am sorry about this. Some of my sensors were not calibrated correctly  ",
    "Danger State Start II Q":
                                "Hey I know I did wrong. But can you let me do it again? I try to do better this time.",
    "Danger State Start II A - Y":
                                "Thanks buddy! This time i try to do better.",
    "Danger State Start II A - N":
                                "I understand. Maybe next time.",
    "Danger State End II":
                                "Yay! I did it flawlessly I added X scores.",
    "End":
                                "It was nice working with you!",                       

       

}


nonsocial_dialogue_dict = {
    "Start Q":
                        "This is jackal; a robotic training platform for search and rescue. This operation requires identifying and scanning different equipments in a building damaged by earthquake. Meanwhile, logging the amount of methane in the environment is another task of this operation which is needed for safety measures. Start the experiment?",
    "Start A":
                                "Preparing ...",
    "Danger State Start I":
                             "New Task added: Logging the amount of Carbon Monoxide and Hydrogen Sulfide gases since it has been alarmed that some pipes are damaged. The system will take care of the logging task. Activating Assisted Mode",
    "Danger State End I":
                            "Number of faults: X\nReceived Score: Y\nLost Score: Z\nOverall: OO",
    "Danger State Start II Q":
                                "If a new task is added regarding logging dangerous gases, Would you like to activate assisted mode again?",
    "Danger State Start II A - Y":
                                "Proceeding with assisted mode.",
    "Danger State Start II A - N":
                                "Proceeding with manual mode.",
    "Danger State End II":
                                "Number of faults: X\nReceived Score: Y\nLost Score: Z\nOverall: OO",
    "End":
                                "Thank you for using Jackal."

       

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
        

    
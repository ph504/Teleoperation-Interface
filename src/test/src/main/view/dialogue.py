from ast import If
from email.policy import default
from re import X
from tkinter import DISABLED, Label, Text


social_mode = True

social_dialogue_dict = {   
    "Start Q":
                        "Hey, I am Jackal! It is amazing that we can work together to save lives eh? So the operation is we have to check for injured people in the building while checking the amount of methane by logging it so people outside can have a better understanding of the situation. Shall we start?",
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
                                "It was nice working with you!"

       

}


nonsocial_dialogue_dict = {
    "Start Q":
                        "This is jackal ... preliminary training for search and rescue. Start the experiment?",
    "Start A":
                                "Preparing ...",
    "Danger State Start I":
                             "... Activating Assisted Mode",
    "Danger State End I":
                            "Number of faults: X\nReceived Score: Y\nLost Score: Z\nOverall: OO",
    "Danger State Start II Q":
                                "... Would you like to activate assisted mode?",
    "Danger State Start II A - Y":
                                "*(Updated) Assisted mode activated!",
    "Danger State Start II A - N":
                                "...",
    "Danger State End II":
                                "Number of faults: X\nReceived Score: Y\nLost Score: Z\nOverall: OO",
    "End":
                                "Thank you for using ..."

       

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
        self.dialogue = social_dialogue_dict[self.state] if social_mode is True else nonsocial_dialogue_dict[self.state]
        self.dialoguetext = Label(root, font=('Calibri',12, 'bold', 'italic'), bg='#e0de99', wraplength= 800)
        self.dialoguetext.config(text= self.dialogue)
        self.dialoguetext.place(x = self.x, y = self.y, width= self.width, height= self.height)

    def change_dialogue(self, string):
        self.state = string
        self.dialogue = social_dialogue_dict[self.state] if social_mode is True else nonsocial_dialogue_dict[self.state]
        self.dialoguetext.config(text= self.dialogue)

    
from tkinter import Tk
from avatar import AvatarModel, AvatarView
from dialogue import *
from avatar import *
from avalogue import *



csv_dialogue = "/home/pouya/catkin_ws/src/test/src/spreadsheets/dialogue_spreadsheet_linux.csv"
csv_idle = "/home/pouya/catkin_ws/src/test/src/spreadsheets/IdleAvatars.csv"
csv_talking = "/home/pouya/catkin_ws/src/test/src/spreadsheets/TalkingAvatars.csv"
csv_reactive = "/home/pouya/catkin_ws/src/test/src/spreadsheets/ReactiveAvatars.csv"


#Dumb combination of avatar and dialogue. it makes sense to me so it doesn't matter

def main():
    window = Tk()
    window.title("Test")
    
    window.configure(width= 1000, height=500)

    d_model = DialogueModel(window, csv_filepath= csv_dialogue)
    d_view = DialogueView(window, dialogueview_info)
    d_controller = DialogueController(window, d_model, d_view)

    a_model = AvatarModel(csv_idle_filepath= csv_idle, csv_talking_filepath= csv_talking, csv_reactive_filepath= csv_reactive)
    a_view = AvatarView(window, avatar_info)
    a_controller = AvatarController(window, a_model, a_view)

    controller = AvalogueController(window,d_model,d_view, a_model,a_view)
    
    def err():
        controller.set_avalogue("t_sad", "choice")
        

    
    def yes():
        controller.set_avalogue("r_happy","congrats")

    def no():
        controller.set_avalogue("r_sad","sorry")


    utils.register("Start" , err)
    
    utils.register("Yes" , yes)
    utils.register("No" , no)

    #d_controller.set_dialogue("start_q_s")
    
    controller.set_avalogue("t_default","start_q_s")


    def on_key_press(event):
        if event.char.lower() == 'h':
            controller.set_avalogue("r_happy","congrats")
        if event.char.lower() == 's':
            controller.set_avalogue("r_sad","sorry")
    
    window.bind('<Key>', on_key_press)
    window.mainloop()




if __name__=="__main__":
    main()





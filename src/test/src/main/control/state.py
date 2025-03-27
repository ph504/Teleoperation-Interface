import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/')

from statemachine import State, StateMachine
import playsound
import time
import threading
from main.control import event_manager
from main.utils import logger
from main.utils import utils
from main.data import global_config as gv

#https://lucid.app/lucidchart/9bb1bf19-cce4-4f60-bbae-7a752431570e/edit?viewport_loc=-315%2C-960%2C2760%2C2400%2C0_0&invitationId=inv_32ea1377-4a91-40f0-9b16-40a05b0fa630

class TeleopGUIMachine(StateMachine):


    def __init__(self, widgets) -> None:
        super().__init__()
        self.timer_canvas = widgets['timer_canvas']
        self.avalogue = widgets['avalogue']
        self.dialogue_text = widgets['dialogue_text']
        self.camera_front = widgets['camera_front']
        self.jackal_ai = widgets['jackal_ai']
        self.countdown = widgets['countdown']
        utils.register("Start", self.initializing_to_start)
        self.jackal_ai.disable()

    #states
    state_initializing = State('state_initializing', initial= True) 
    state_start = State('state_start') #Start 
    state_termination = State('state_termination') #End

    initializing_to_start = state_initializing.to(state_start) #Start 
    start_to_danger1_start = state_start.to(state_danger1_start) #Danger Start I 
    danger3_end_to_termination = state_danger3_end.to(state_termination) #End

    def sens_calib_cmplt(self):
        time.sleep(30)
        self.avalogue.set_avalogue('t_default', "sens_calib")

    def danger_warning(self):
        time.sleep(20)
        self.avalogue.set_avalogue("t_default", "danger_w")

    def unfrezee_delay(self):
        time.sleep(5)
        EventManager.post_event("unfreeze", -1) # type: ignore

    #state_start --- Start
    def on_initializing_to_start (self):
        def start():
            print("***state_start --- Start***")
            event_manager.EventManager.post_event("unfreeze", -1) # type: ignore
            event_manager.EventManager.post_event("start_move_bars", -1) # type: ignore
            self.timer.start()
            self.avalogue.set_avalogue("r_happy", "start_a")
  
        x = threading.Thread(target= start)
        x.start() 
                        
     
    def start_cntdwn(self, dummy = 0):
        self.countdown_canvas.start_countdown()


class TutorialGUIMachine(StateMachine):
    
    def __init__(self, widgets) -> None:
        super().__init__()
        
        self.timer = widgets['timer_canvas']
        self.jackal_ai = widgets['jackal_ai']
        self.avalogue = widgets['avalogue']

        utils.register("Start", self.initializing_to_start)

    state_initializing = State('state_initializing', initial= True) 
    state_start = State('state_start') #Start 

    initializing_to_start = state_initializing.to(state_start) #Start 
    start_to_danger1_start = state_start.to(state_danger1_start) #Danger Start I 
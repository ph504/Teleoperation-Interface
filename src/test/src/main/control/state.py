import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/model/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/control/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/view/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/utils/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/test/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/data/')

from statemachine import State, StateMachine
import playsound
import time
import threading
import event_manager
from logger import Logger
import global_config as gv
import test.src.main.utils.utils as utils


#https://lucid.app/lucidchart/9bb1bf19-cce4-4f60-bbae-7a752431570e/edit?viewport_loc=-315%2C-960%2C2760%2C2400%2C0_0&invitationId=inv_32ea1377-4a91-40f0-9b16-40a05b0fa630

class TeleopGUIMachine(StateMachine):


    def __init__(self,
                timer,
                avalogue,
                dialogue,
                nmode_btn,
                amode_btn,
                jackal_avatar,
                flashing_image,
                tsk_cnvs,
                cmr_frm,
                jckl_ai,
                cntdwn) -> None:
        super().__init__()
        self.timer = timer
        self.avalogue = avalogue
        self.dialogue = dialogue
        self.normalmode_button = nmode_btn
        self.assistedmode_button = amode_btn
        self.javatar = jackal_avatar
        self.flashing_image = flashing_image
        self.is_ai = False
        self.task_canvas = tsk_cnvs
        self.is_yes = None
        self.camera_frame = cmr_frm
        self.jackal_ai = jckl_ai
        self.countdown_canvas = cntdwn
        utils.register("Start", self.initializing_to_start)
        utils.register("Yes", self.on_yes)
        utils.register("No", self.on_no)

       
        self.jackal_ai.disable()
        EventManager.subscribe("start_cntdwn", self.start_cntdwn) # type: ignore

    #states
    state_initializing = State('state_initializing', initial= True) 
    state_start = State('state_start') #Start 
    state_danger1_start = State('state_danger1_start') #Danger Start I
    state_danger1_end = State('state_danger1_end') #Danger End I
    state_danger2_start = State('state_danger2_start') #Danger Start II
    state_danger2_end = State('state_danger2_end') #Danger End II
    state_decision_prompt = State('state_decision_prompt') #Choice Q
    state_decision_outcome = State('state_decision_outcome') #Choice A Y/N
    state_danger3_start = State('state_danger3_start') #Danger State Start III Y / Danger State Start III N
    state_danger3_end = State('state_danger3_end') #Danger State End III Y / Danger State End III N
    state_termination = State('state_termination') #End

    initializing_to_start = state_initializing.to(state_start) #Start 
    start_to_danger1_start = state_start.to(state_danger1_start) #Danger Start I 
    danger1_start_to_danger1_end = state_danger1_start.to(state_danger1_end) #Danger End I
    danger1_end_to_danger2_start = state_danger1_end.to(state_danger2_start) #Danger Start II
    danger2_start_to_danger2_end = state_danger2_start.to(state_danger2_end) #Danger End II
    danger2_end_to_decision_prompt = state_danger2_end.to(state_decision_prompt) #Choice Q
    decision_prompt_to_decision_outcome = state_decision_prompt.to(state_decision_outcome) #Choice A Y/N
    decision_outcome_to_danger3_start = state_decision_outcome.to(state_danger3_start) #Danger State Start III Y / Danger State Start III N
    danger3_start_to_danger3_end = state_danger3_start.to(state_danger3_end) #Danger State End III Y / Danger State End III N
    danger3_end_to_termination = state_danger3_end.to(state_termination) #End

    DANGER_START_TIMER = 10
    DANGER_END_TIMER = 10
    COLOR_TRANS_TIMER = 30
    WARNING_TIMER = 15   

    def assistedmanual_disable(self):
        EventManager.post_event("count_manual_trans_deactive", -1) # type: ignore
        self.flashing_image.disable()
        self.assistedmode_button.disable()
        self.normalmode_button.disable()
        self.jackal_ai.disable()

    def normal_activate(self):
        EventManager.post_event("count_manual_trans_active", -1) # type: ignore
        self.flashing_image.enable()
        #playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
        gv.danger_alarm_sound.play()
        self.assistedmode_button.disable()
        self.normalmode_button.enable()
        self.jackal_ai.disable()

    def assisted_activate(self):
        self.flashing_image.enable()
        #playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
        gv.danger_alarm_sound.play()
        self.assistedmode_button.enable()
        self.normalmode_button.disable()
        self.jackal_ai.enable()

    def sens_calib_cmplt(self):
        time.sleep(30)
        self.avalogue.set_avalogue('t_default', "sens_calib")

    def danger_warning(self):
        time.sleep(20)
        self.avalogue.set_avalogue("t_default", "danger_w")

    def unfrezee_delay(self):
        time.sleep(5)
        EventManager.post_event("unfreeze", -1) # type: ignore
    
    def danger_fail(self):
        time.sleep(15)
        self.avalogue.set_avalogue("t_sad", "danger_fail")

    #state_start --- Start
    def on_initializing_to_start (self):
        def start():
            print("***state_start --- Start***")
            EventManager.post_event("unfreeze", -1) # type: ignore
            EventManager.post_event("start_move_bars", -1) # type: ignore
            self.timer.start()
            self.avalogue.set_avalogue("r_happy", "start_a")
  
        x = threading.Thread(target= start)
        x.start() 
                        
    #state_danger1_start --- Danger Start I
    def on_start_to_danger1_start (self): 
        def danger_start1():
            print("***state_danger1_start --- Danger Start I***")
            time.sleep(self.DANGER_START_TIMER)

            self.avalogue.set_avalogue("t_default", "danger_s1")
            Logger.log("danger_zone_start", "ai_handler") # type: ignore
            self.assisted_activate()
            x = threading.Thread(target=self.danger_timer_countdown_s2)
            x.start()
           
        y = threading.Thread(target=danger_start1)
        y.start()
        
    #state_danger1_end --- Danger End I
    def on_danger1_start_to_danger1_end (self): 
        def danger_end1():
            print("***state_danger1_end --- Danger End I***")
            time.sleep(self.DANGER_END_TIMER)    
            self.avalogue.set_avalogue("t_sad", "danger_e1")


            Logger.log("danger_zone_end", "ai_handler") # type: ignore
            
            
            self.assistedmanual_disable()

            x = threading.Thread(target=self.sens_calib_cmplt)
            x.start()
            
        x = threading.Thread(target=danger_end1)
        x.start()
 
    #state_danger2_start --- Danger Start II
    def on_danger1_end_to_danger2_start(self): 
        def danger_start2():
            print("***state_danger2_start --- Danger Start II***")
            time.sleep(self.DANGER_START_TIMER)
            
            self.avalogue.set_avalogue("t_default", "danger_s2")
            self.normal_activate()

            Logger.log("danger_zone_start", "operator_handler") # type: ignore

            x = threading.Thread(target=self.danger_timer_countdown_s3)
            x.start()
            
        a = threading.Thread(target=danger_start2)
        a.start()
     
    # TODO wtf 
    def on_yes(self):
        
        if self.is_yes == None:
            print("YESSS")
            self.is_yes = True
            Logger.log("CHOICE", "YES") # type: ignore
            self.decision_prompt_to_decision_outcome()
        
    def on_no(self):
        if self.is_yes == None:
            print("NOOOO")
            self.is_yes = False
            Logger.log("CHOICE", "NO") # type: ignore
            self.decision_prompt_to_decision_outcome()  
     
    def start_cntdwn(self, dummy = 0):
        self.countdown_canvas.start_countdown()

    #state_danger2_end --- #Danger End II
    def on_danger2_start_to_danger2_end (self):
        def danger_end2():
            print("***state_danger2_end --- #Danger End II***")
            time.sleep(self.DANGER_END_TIMER/2)
            time.sleep(self.DANGER_END_TIMER)
            self.avalogue.set_avalogue("t_default", "danger_e2")

            self.assistedmanual_disable()
            Logger.log("danger_zone_end", "operator_handler") # type: ignore

            x = threading.Thread(target=self.danger_fail)
            x.start()
            

            self.danger2_end_to_decision_prompt()

        x = threading.Thread(target=danger_end2)
        x.start()

    #state_decision_prompt --- Choice Q
    def on_danger2_end_to_decision_prompt (self): 
        def choice_q():
           #sleep for 30 seconds
           time.sleep(35)
           print("***state_decision_prompt --- Choice Q***")
           #---
           #show avalogue
           EventManager.post_event("freeze", -1) # type: ignore
           self.avalogue.set_avalogue("t_default", "choice_q")

           

           # ---
           # after finishing dialogue (?) show a countdown for 30 seconds (?)
           self.countdown_canvas.enable()
           # ---
           
           # after 30 seconds it should freeze (show a new dialogue?) and validate should also freeze 
                
        x= threading.Thread(target=choice_q)
        x.start()
          
    def danger_timer_countdown_s2(self):
        time.sleep(180)
        
        #Danger End I/ time-check
        if self.is_s2:
            self.danger1_start_to_danger1_end()

    def danger_timer_countdown_s3(self):
        time.sleep(180)
        
        #Danger End II/  time-check
        if self.is_s3:
            self.danger1_end_to_danger2_start()

    def danger_timer_countdown_s7(self):
        time.sleep(180)
        
        #Danger End III/ time-check
        if self.is_s7:
            self.decision_outcome_to_danger3_start()

    #state_decision_outcome --- Choice A Y/N
    def on_decision_prompt_to_decision_outcome (self): 
        
        def choice_yn():
            print("***state_decision_outcome --- Choice A Y/N***")
            EventManager.post_event("clear_wait_flag", -1) # type: ignore
            EventManager.post_event("unfreeze", -1) # type: ignore
            self.countdown_canvas.disable()

            if self.is_yes:
                EventManager.post_event("assisted_second", -1) # type: ignore
                self.avalogue.set_avalogue("r_happy", "choice_y")
                self.is_ai = True 
            else:
                EventManager.post_event("manual_second", -1) # type: ignore
                self.avalogue.set_avalogue("t_default", "choice_n")
                self.is_ai = False

            x = threading.Thread(target= self.unfrezee_delay)
            x.start()
        x = threading.Thread(target=choice_yn)
        x.start()

    #state_danger3_start --- Danger State Start III Y / Danger State Start III N
    def on_decision_outcome_to_danger3_start (self):
        def danger_start3y():
            print("***state_danger3_start --- Danger State Start III Y / Danger State Start III N***")
            time.sleep(self.DANGER_START_TIMER)
            
            self.avalogue.set_avalogue("r_happy", "danger_s3y")

            Logger.log("danger_zone_start", "ai_handler") # type: ignore
            
            self.assisted_activate()

            x = threading.Thread(target=self.danger_timer_countdown_s7)
            x.start()
        
        def dangerstart3n():

            time.sleep(self.DANGER_START_TIMER)



            self.avalogue.set_avalogue("t_default", "danger_s3n")

            

            Logger.log("danger_zone_start", "operator_handler") # type: ignore
            
            self.normal_activate()

            x = threading.Thread(target=self.danger_timer_countdown_s7)
            x.start()
        
        if self.is_ai:
            y = threading.Thread(target=danger_start3y)
            y.start()
        else:
            n = threading.Thread(target=dangerstart3n)
            n.start()

    #state_danger3_end --- Danger State End III Y / Danger State End III N
    def on_danger3_start_to_danger3_end(self):
        def danger_end3():
            time.sleep(self.DANGER_END_TIMER)
            print("***state_danger3_end --- Danger State End III Y / Danger State End III N***")
            if self.is_ai:
                self.avalogue.set_avalogue("t_default", "danger_e3y")
                self.assistedmanual_disable()        
                Logger.log("danger_zone_end", "ai_handler")        # type: ignore
            else:
                self.avalogue.set_avalogue("t_default", "danger_e3n")

                
                self.assistedmanual_disable()
                
                

                Logger.log("danger_zone_end", "operator_handler") # type: ignore
                
                
        x = threading.Thread(target=danger_end3)
        x.start() 
        
    #state_termination --- End
    def on_danger3_end_to_termination(self):
        self.timer.stop()
        print("***state_termination --- End***")
        self.avalogue.set_avalogue("t_default", "end")
        Logger.log("end", "N/A") # type: ignore
        EventManager.post_event("task_count", self.task_canvas.count) # type: ignore
        gv.bar_controller = True
        EventManager.post_event("stop_move_bars", -1) # type: ignore

class TutorialGUIMachine(StateMachine):
    
    def __init__(self,timer,
                nmode_btn,
                amode_btn,
                flashing_image,
                jckl_ai,
                avalogue) -> None:
        super().__init__()
        self.timer = timer
        self.flashing_image = flashing_image
        self.assistedmode_button = amode_btn
        self.normalmode_button = nmode_btn
        self.jackal_ai = jckl_ai
        self.avalogue = avalogue
        utils.register("Start", self.initializing_to_start)

    state_initializing = State('state_initializing', initial= True) 
    state_start = State('state_start') #Start 
    state_danger1_start = State('state_danger1_start') #Danger Start I / Manual Mode
    state_danger1_end = State('state_danger1_end') #Danger End I / Manual Mode
    state_danger2_start = State('state_danger2_start') #End

    initializing_to_start = state_initializing.to(state_start) #Start 
    start_to_danger1_start = state_start.to(state_danger1_start) #Danger Start I 
    danger1_start_to_danger1_end = state_danger1_start.to(state_danger1_end) #Danger End I
    danger1_end_to_danger2_start = state_danger1_end.to(state_danger2_start) #End
    
    DANGER_START_TIMER = 10
    DANGER_END_TIMER = 10


    def assistedmanual_disable(self):
        EventManager.post_event("count_manual_trans_deactive", -1) # type: ignore
        self.flashing_image.disable()
        self.assistedmode_button.disable()
        self.normalmode_button.disable()
        self.jackal_ai.disable()
    
    def normal_activate(self):
        EventManager.post_event("count_manual_trans_active", -1) # type: ignore
        self.flashing_image.enable()
        #playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
        gv.danger_alarm_sound.play()
        self.assistedmode_button.disable()
        self.normalmode_button.enable()
        self.jackal_ai.disable()

    def danger_warning_tutorial(self):
        time.sleep(15)
        self.avalogue.set_avalogue("t_default", "t_danger_w")

    def on_initializing_to_start(self):
        EventManager.post_event("unfreeze", -1) # type: ignore
        gv.bar_controller = False
        EventManager.post_event("start_move_bars", -1) # type: ignore
        self.avalogue.set_avalogue("r_happy", "t_start_a")
        
        self.timer.start()
        
        x = threading.Thread(target=self.danger_warning_tutorial)
        x.start()
            
    def on_start_to_danger1_start(self):
        def danger_start():
            time.sleep(self.DANGER_START_TIMER)
            self.normal_activate()
            self.avalogue.set_avalogue("t_default", "t_danger_s")

        x = threading.Thread(target=danger_start)
        x.start()

    def on_danger1_start_to_danger1_end(self):
        def danger_end():
            time.sleep(self.DANGER_END_TIMER)
            self.assistedmanual_disable()
            self.avalogue.set_avalogue("t_default", "t_danger_e")

        x = threading.Thread(target=danger_end)
        x.start()
        
    def on_danger1_end_to_danger2_start(self):
        self.timer.stop()
        gv.bar_controller = True
        EventManager.post_event("stop_move_bars", -1) # type: ignore
        self.avalogue.set_avalogue("t_default", "t_end")
        
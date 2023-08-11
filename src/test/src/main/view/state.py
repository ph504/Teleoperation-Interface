from statemachine import State, StateMachine
from view import switch_danger
from playsound import *
import time
import threading
from event import *
from logger import Logger
import global_variables
import utils


#https://lucid.app/lucidchart/9bb1bf19-cce4-4f60-bbae-7a752431570e/edit?viewport_loc=-315%2C-960%2C2760%2C2400%2C0_0&invitationId=inv_32ea1377-4a91-40f0-9b16-40a05b0fa630

class TeleopGUIMachine(StateMachine):


    def __init__(self,
                timer,
                avalogue,
                dialogue,
                nmode_btn,
                amode_btn,
                n_bar,
                d_bars,
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
        self.normal_bar = n_bar
        self.danger_bars = d_bars
        self.javatar = jackal_avatar
        self.flashing_image = flashing_image
        self.is_ai = False
        self.task_canvas = tsk_cnvs
        self.is_yes = None
        self.camera_frame = cmr_frm
        self.jackal_ai = jckl_ai
        self.countdown_canvas = cntdwn
        utils.register("Start", self.s01)
        utils.register("Yes", self.on_yes)
        utils.register("No", self.on_no)

       
        self.jackal_ai.disable()
        EventManager.subscribe("start_cntdwn", self.start_cntdwn)

    #states
    s0 = State('S0', initial= True) 
    s1 = State('S1') #Start 
    s2 = State('S2') #Danger Start I
    s3 = State('S3') #Danger End I
    s4 = State('S4') #Danger Start II
    s5 = State('S5') #Danger End II
    s6 = State('S6') #Choice Q
    s7 = State('S7') #Choice A Y/N
    s8 = State('S8') #Danger State Start III Y / Danger State Start III N
    s9 = State('S9') #Danger State End III Y / Danger State End III N
    s10 = State('S10') #End

    s01 = s0.to(s1) #Start 
    s12 = s1.to(s2) #Danger Start I 
    s23 = s2.to(s3) #Danger End I
    s34 = s3.to(s4) #Danger Start II
    s45 = s4.to(s5) #Danger End II
    s56 = s5.to(s6) #Choice Q
    s67 = s6.to(s7) #Choice A Y/N
    s78 = s7.to(s8) #Danger State Start III Y / Danger State Start III N
    s89 = s8.to(s9) #Danger State End III Y / Danger State End III N
    s910 = s9.to(s10) #End

    DANGER_START_TIMER = 10
    DANGER_END_TIMER = 10
    COLOR_TRANS_TIMER = 30
    WARNING_TIMER = 15   

    def assistedmanual_disable(self):
        EventManager.post_event("count_manual_trans_deactive", -1)
        switch_danger(self.normal_bar, self.danger_bars)
        self.flashing_image.disable()
        self.assistedmode_button.disable()
        self.normalmode_button.disable()
        self.jackal_ai.disable()

    def normal_activate(self):
        switch_danger(self.normal_bar, self.danger_bars)
        EventManager.post_event("count_manual_trans_active", -1)
        self.flashing_image.enable()
        playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
        self.assistedmode_button.disable()
        self.normalmode_button.enable()
        self.jackal_ai.disable()

    def assisted_activate(self):
        switch_danger(self.normal_bar, self.danger_bars)
        self.flashing_image.enable()
        playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
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
        EventManager.post_event("unfreeze", -1)
    
    def danger_fail(self):
        time.sleep(15)
        self.avalogue.set_avalogue("t_sad", "danger_fail")

    #S1 --- Start
    def on_s01 (self):
        def start():
        
            EventManager.post_event("unfreeze", -1)
            EventManager.post_event("start_move_bars", -1)
            self.timer.start()
            
            #self.dialogue.change_dialogue("Start A") 
            self.avalogue.set_avalogue("r_happy", "start_a")

            
            
            #if global_variables.social_mode:
                #self.javatar.change_image_happy()
            
            #TODO: use after function to 
            x = threading.Thread(target=self.danger_warning)
            x.start()
            self.normal_bar.start()
        
        x = threading.Thread(target= start)
        x.start() 
         
         
        
    #S2 --- Danger Start I
    def on_s12 (self): 
        def danger_start1():
            
            time.sleep(self.DANGER_START_TIMER)

            self.avalogue.set_avalogue("t_default", "danger_s1")


            Logger.log("danger_zone_start", "ai_handler")
            self.assisted_activate()
            x = threading.Thread(target=self.danger_timer_countdown_s2)
            x.start()
           
        y = threading.Thread(target=danger_start1)
        y.start()
        
    #S3 --- Danger End I
    def on_s23 (self): 
        def danger_end1():
            time.sleep(self.DANGER_END_TIMER)
            
            if not global_variables.second_round:
               self.avalogue.set_avalogue("t_sad", "danger_e1_1")
            else:
                self.avalogue.set_avalogue("t_sad", "danger_e1_2")

            Logger.log("danger_zone_end", "ai_handler")
            
            
            self.assistedmanual_disable()

        
        x = threading.Thread(target=danger_end1)
        x.start()
 
    #S4 --- Danger Start II
    def on_s34(self): 
        def danger_start2():
            
            time.sleep(self.DANGER_START_TIMER)
            
            self.avalogue.set_avalogue("t_default", "danger_s2")
            self.normal_activate()

            Logger.log("danger_zone_start", "operator_handler")

            x = threading.Thread(target=self.danger_timer_countdown_s3)
            x.start()
            
        a = threading.Thread(target=danger_start2)
        a.start()
     
    def on_yes(self):
        
        if self.is_yes == None:
            print("YESSS")
            self.is_yes = True
            Logger.log("CHOICE", "YES")
            self.s67()
        
    def on_no(self):
        if self.is_yes == None:
            print("NOOOO")
            self.is_yes = False
            Logger.log("CHOICE", "NO")
            self.s67()  
     
    def start_cntdwn(self, dummy = 0):
        self.countdown_canvas.start_countdown()

    #S5 --- #Danger End II
    def on_s45 (self):
        def danger_end2():
            
            time.sleep(self.DANGER_END_TIMER/2)
            time.sleep(self.DANGER_END_TIMER)
            
            if not global_variables.second_round:
                self.avalogue.set_avalogue("t_default", "danger_e2_1")
            else:
                self.avalogue.set_avalogue("t_default", "danger_e2_2")
            
            
            self.assistedmanual_disable()
            Logger.log("danger_zone_end", "operator_handler")

            x = threading.Thread(target=self.danger_fail)
            x.start()
            

            self.s56()

        x = threading.Thread(target=danger_end2)
        x.start()

    #S6 --- Choice Q
    def on_s56 (self): 
        def choice_q():
           #sleep for 30 seconds
           time.sleep(35)
           #---
           #show avalogue
           EventManager.post_event("freeze", -1)
           if not global_variables.second_round:
                self.avalogue.set_avalogue("t_default", "choice_q_1")
           else:
                self.avalogue.set_avalogue("t_default", "choice_q_2")
           

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
            self.s23()

    def danger_timer_countdown_s3(self):
        time.sleep(180)
        
        #Danger End II/  time-check
        if self.is_s3:
            self.s34()

    def danger_timer_countdown_s7(self):
        time.sleep(180)
        
        #Danger End III/ time-check
        if self.is_s7:
            self.s78()


    #S7 --- Choice A Y/N
    def on_s67 (self): 
        
        def choice_yn():
            EventManager.post_event("clear_wait_flag", -1)
            EventManager.post_event("unfreeze", -1)
            self.countdown_canvas.disable()

            if self.is_yes:
                EventManager.post_event("assisted_second", -1)
                self.avalogue.set_avalogue("r_happy", "choice_y")
                self.is_ai = True 
            else:
                EventManager.post_event("manual_second", -1)
                self.avalogue.set_avalogue("t_default", "choice_n")
                self.is_ai = False

            x = threading.Thread(target= self.unfrezee_delay)
            x.start()
        x = threading.Thread(target=choice_yn)
        x.start()

    #S8 --- Danger State Start III Y / Danger State Start III N
    def on_s78 (self):
        def danger_start3y():
            
            time.sleep(self.DANGER_START_TIMER)
            
            self.avalogue.set_avalogue("r_happy", "danger_s3y")

            Logger.log("danger_zone_start", "ai_handler")
            
            self.assisted_activate()

            x = threading.Thread(target=self.danger_timer_countdown_s7)
            x.start()
        
        def dangerstart3n():

            time.sleep(self.DANGER_START_TIMER)



            self.avalogue.set_avalogue("t_default", "danger_s3n")

            

            Logger.log("danger_zone_start", "operator_handler")
            
            self.normal_activate()

            x = threading.Thread(target=self.danger_timer_countdown_s7)
            x.start()
        
        if self.is_ai:
            y = threading.Thread(target=danger_start3y)
            y.start()
        else:
            n = threading.Thread(target=dangerstart3n)
            n.start()


    #S9 --- Danger State End III Y / Danger State End III N
    def on_s89(self):
        def danger_end3():
            time.sleep(self.DANGER_END_TIMER)
            
            if self.is_ai:
                if global_variables.second_round:
                    self.avalogue.set_avalogue("t_default", "danger_e3y_1")
                else:
                    self.avalogue.set_avalogue("t_default", "danger_e3y_2")

                self.assistedmanual_disable()        

                Logger.log("danger_zone_end", "ai_handler")       
            else:
                
                if global_variables.second_round:
                    self.avalogue.set_avalogue("t_default", "danger_e3n_1")
                else:
                    self.avalogue.set_avalogue("t_default", "danger_e3n_2")

                
                self.assistedmanual_disable()
                
                

                Logger.log("danger_zone_end", "operator_handler")
                
                
        x = threading.Thread(target=danger_end3)
        x.start() 
        
    #S10 --- End
    def on_s910(self):
        self.timer.stop()
        self.avalogue.set_avalogue("t_default", "end")
        Logger.log("end", "N/A")
        EventManager.post_event("task_count", self.task_canvas.count)
        global_variables.bar_controller = True
        EventManager.post_event("stop_move_bars", -1)

class TutorialGUIMachine(StateMachine):
    def __init__(self,timer,
                nmode_btn,
                amode_btn,
                n_bar,
                flashing_image,
                d_bars,
                jckl_ai) -> None:
        super().__init__()
        self.timer = timer
        self.normal_bar = n_bar
        self.danger_bars = d_bars
        self.flashing_image = flashing_image
        self.assistedmode_button = amode_btn
        self.normalmode_button = nmode_btn
        self.jackal_ai = jckl_ai

    s0 = State('S0', initial= True) 
    s1 = State('S1') #Start 
    s2 = State('S2') #Danger Start I / Manual Mode
    s3 = State('S3') #Danger End I / Manual Mode
    s4 = State('S4') #End

    s01 = s0.to(s1) #Start 
    s12 = s1.to(s2) #Danger Start I 
    s23 = s2.to(s3) #Danger End I
    s34 = s3.to(s4) #End
    
    DANGER_START_TIMER = 10
    DANGER_END_TIMER = 10


    def assistedmanual_disable(self):
        EventManager.post_event("count_manual_trans_deactive", -1)
        switch_danger(self.normal_bar, self.danger_bars)
        self.flashing_image.disable()
        self.assistedmode_button.disable()
        self.normalmode_button.disable()
        self.jackal_ai.disable()
    
    def normal_activate(self):
        switch_danger(self.normal_bar, self.danger_bars)
        EventManager.post_event("count_manual_trans_active", -1)
        self.flashing_image.enable()
        playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
        self.assistedmode_button.disable()
        self.normalmode_button.enable()
        self.jackal_ai.disable()

    def on_s01(self):
        global_variables.bar_controller = False
        EventManager.post_event("start_move_bars", -1)
        self.timer.start()
            
    def on_s12(self):
        def danger_start():
            time.sleep(self.DANGER_START_TIMER)
            self.normal_activate()

        x = threading.Thread(target=danger_start)
        x.start()

    def on_s23(self):
        def danger_end():
            time.sleep(self.DANGER_END_TIMER)
            self.assistedmanual_disable()

        x = threading.Thread(target=danger_end)
        x.start()
        
    def on_s34(self):
        self.timer.stop()
        global_variables.bar_controller = True
        EventManager.post_event("stop_move_bars", -1)
        
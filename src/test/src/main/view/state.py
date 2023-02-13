from statemachine import State, StateMachine
from view import switch_danger
from dialogue import social_mode
from playsound import *
import time
import threading
from event import *



#https://lucid.app/lucidchart/9bb1bf19-cce4-4f60-bbae-7a752431570e/edit?viewport_loc=-315%2C-960%2C2760%2C2400%2C0_0&invitationId=inv_32ea1377-4a91-40f0-9b16-40a05b0fa630

class TeleopGUIMachine(StateMachine):
    def __init__(self,
                timer,
                dialogue,
                start_btn,
                y_btn,
                n_btn,
                nmode_btn,
                amode_btn,
                n_bar,
                d_bars,
                jackal_avatar,
                flashing_image,
                tsk_cnvs) -> None:
        super().__init__()
        self.timer = timer
        self.dialogue = dialogue
        self.start_button = start_btn
        self.yes_button = y_btn
        self.no_button = n_btn
        self.normalmode_button = nmode_btn
        self.assistedmode_button = amode_btn
        self.normal_bar = n_bar
        self.danger_bars = d_bars
        self.javatar = jackal_avatar
        self.flashing_image = flashing_image
        self.is_ai = False
        self.task_canvas = tsk_cnvs
        self.is_yes = False

    #states
    s0 = State('S0', initial= True)
    s1 = State('S1')
    s2 = State('S2')
    s3 = State('S3')
    s4 = State('S4')
    s5 = State('S5')
    s6 = State('S6')
    s7 = State('S7')
    s8 = State('S8')


    s01 = s0.to(s1)
    s11 = s1.to(s1) 
    s12 = s1.to(s2)
    s23 = s2.to(s3)
    s34 = s3.to(s4)
    s45 = s4.to(s5)
    s46 = s4.to(s6)
    s57 = s5.to(s7)
    s67 = s6.to(s7)
    s78 = s7.to(s8)

    #S1
    def on_s01 (self):
        self.timer.start()
        self.dialogue.change_dialogue("Start A") #happy for 30 seconds!
        if social_mode:
             self.javatar.change_image_temp("happy")
        self.start_button.deactivate()
        self.normal_bar.start()
        x = threading.Thread(target=self.warning_1)
        x.start()
        
    
    def warning_1(self):
        time.sleep(45)
        self.dialogue.change_dialogue('Danger State Warning I')

    #S2
    def on_s12 (self): 
        def danger_start1():
            time.sleep(20)
            self.dialogue.change_dialogue("Danger State Start I") #default
            playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block=False)
            self.flashing_image.enable()
            switch_danger(self.normal_bar, self.danger_bars)
            self.assistedmode_button.enable()
            self.normalmode_button.disable()
            x = threading.Thread(target=self.danger_timer_countdown)
            x.start()
        y = threading.Thread(target=danger_start1)
        y.start()
        
    #S3
    def on_s23 (self): 
        self.dialogue.change_dialogue("Danger State End I/Warning II Q") #sad because it made some mistakes!
        switch_danger(self.normal_bar, self.danger_bars)
        self.flashing_image.disable()
        self.assistedmode_button.disable()
        self.normalmode_button.enable()
        self.dialogue.change_start_to_yesno()
        self.yes_button.activate()
        self.no_button.activate()


    #delete this since s34 happens via buttons
    def warning_2(self):
        time.sleep(45)
        self.s34()
    
    #S4 
    def on_s34(self): 
        if self.is_yes:
            self.dialogue.change_dialogue("Danger State Warning II A-Y")
            self.is_ai = True
            self.yes_button.deactivate()
            self.no_button.deactivate()
        else:
            self.dialogue.change_dialogue("Danger State Warning II A-N")
            self.is_ai = False
            self.yes_button.deactivate()
            self.no_button.deactivate()
    
    def on_yes(self):
        self.is_yes = True
        self.s34()

        
    def on_no(self):
        self.is_yes = False
        self.s34()  

        
    #S5
    def on_s45 (self): 
        def danger_start2y():
            time.sleep(20)
            self.dialogue.change_dialogue("Danger State Start II Y") #happy for 20 seconds
            playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
            self.flashing_image.enable()
            if social_mode:
                self.javatar.change_image_temp("happy")
            switch_danger(self.normal_bar, self.danger_bars)
            self.assistedmode_button.enable()
            self.normalmode_button.disable()
            x = threading.Thread(target=self.danger_timer_countdown)
            x.start()
        y = threading.Thread(target=danger_start2y)
        y.start()
    #S6
    def on_s46 (self): 
        def dangerstart2n():
            time.sleep(20)
            self.dialogue.change_dialogue("Danger State Start II N") #sad for 20 seconds
            playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
            self.flashing_image.enable()
            if social_mode:
                self.javatar.change_image_temp("sad")
            switch_danger(self.normal_bar, self.danger_bars)
            x = threading.Thread(target=self.danger_timer_countdown)
            x.start()
        y = threading.Thread(target=dangerstart2n)
        y.start()

    
    def danger_timer_countdown(self):
        time.sleep(180)
        if self.is_s2:
            self.s23()
        elif self.is_s5:
            self.s57()
        elif self.is_s6:
            self.s67()

    #S7
    def on_s57 (self): 
        self.dialogue.change_dialogue("Danger State End II Y") #default
        switch_danger(self.normal_bar, self.danger_bars)
        self.flashing_image.disable()
        self.assistedmode_button.disable()
        self.normalmode_button.enable()
    #S7
    def on_s67 (self): 
        self.dialogue.change_dialogue("Danger State End II N") #default
        self.flashing_image.disable()
        switch_danger(self.normal_bar, self.danger_bars) 
    #S8
    def on_s78 (self):
        self.timer.stop()
        self.dialogue.change_dialogue("End") #default
        post_event("task_count", self.task_canvas.count)

    




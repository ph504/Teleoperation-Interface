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
                tsk_cnvs,
                circle_cnvs) -> None:
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
        self.circle_canvas = circle_cnvs

    #states
    s0 = State('S0', initial= True) 
    s1 = State('S1') #Start 
    s2 = State('S2') #Danger Start I
    s3 = State('S3') #Danger End I
    s4 = State('S4') #Danger Start II
    s5 = State('S5') #Danger End II/ Warning II Q
    s6 = State('S6') #Danger State Warning II A-Y/A-N
    s7 = State('S7') #Danger State Start III Y / Danger State Start III N
    s8 = State('S8') #Danger State End III Y / Danger State End Y
    s9 = State('S9') #End

    s01 = s0.to(s1) #Start 
    s12 = s1.to(s2) #Danger Start I 
    s23 = s2.to(s3) #Danger End I
    s34 = s3.to(s4) #Danger Start II
    s45 = s4.to(s5) #Danger End II/ Warning II Q
    s56 = s5.to(s6) #Danger State Warning II A-Y/A-N
    s67 = s6.to(s7) #Danger State Start III Y / Danger State Start III N
    s78 = s7.to(s8) #Danger State End III Y / Danger State End III Y
    s89 = s8.to(s9) #End

    #S1 --- Start
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

    #S2 --- Danger Start I
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
        
    #S3 --- Danger End I
    def on_s23 (self): 
        self.dialogue.change_dialogue("Danger State End I")
        switch_danger(self.normal_bar, self.danger_bars)
        self.flashing_image.disable()
        self.assistedmode_button.disable()
        self.normalmode_button.enable()
 
    #S4 --- Danger Start II
    def on_s34(self): 
        def danger_start2():
            time.sleep(20)
            self.dialogue.change_dialogue("Danger State Start II") #happy for 20 seconds
            playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
            self.flashing_image.enable()
            if social_mode:
                self.javatar.change_image_temp("happy")
            switch_danger(self.normal_bar, self.danger_bars)
            self.assistedmode_button.enable()
            self.normalmode_button.disable()
            x = threading.Thread(target=self.danger_timer_countdown)
            x.start()
        a = threading.Thread(target=danger_start2)
        a.start()
    
    def on_yes(self):
        self.is_yes = True
        self.s56()
        
    def on_no(self):
        self.is_yes = False
        self.s56()  
     
    #S5 --- #Danger End II/ Warning II Q
    def on_s45 (self): 
        self.dialogue.change_dialogue("Danger State End II/Warning II Q") #sad because it made some mistakes!
        switch_danger(self.normal_bar, self.danger_bars)
        self.flashing_image.disable()
        self.assistedmode_button.disable()
        self.normalmode_button.enable()
        self.dialogue.change_start_to_yesno()
        self.yes_button.activate()
        self.no_button.activate()

    #S6 --- Danger State Warning II A-Y/A-N
    def on_s56 (self): 
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
          
           
    def danger_timer_countdown(self):
        time.sleep(180)
        
        #Danger End I/ time-check
        if self.is_s2:
            self.s23()

        #Danger End II/  time-check
        elif self.is_s3:
            self.s45()

        #Danger End III/ time-check
        elif self.is_s7:
            self.s78()


    #S7 --- Danger State Start III Y / Danger State Start III N
    def on_s67 (self): 
        def danger_start3y():
            time.sleep(20)
            self.dialogue.change_dialogue("Danger State Start III Y") #happy for 20 seconds
            playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
            self.flashing_image.enable()
            if social_mode:
                self.javatar.change_image_temp("happy")
            switch_danger(self.normal_bar, self.danger_bars)
            self.assistedmode_button.enable()
            self.normalmode_button.disable()
            x = threading.Thread(target=self.danger_timer_countdown)
            x.start()
        def dangerstart3n():
            time.sleep(20)
            self.dialogue.change_dialogue("Danger State Start III N") #sad for 20 seconds
            playsound("/home/pouya/catkin_ws/src/test/src/sounds/danger-alarm.wav", block= False)
            self.flashing_image.enable()
            if social_mode:
                self.javatar.change_image_temp("sad")
            switch_danger(self.normal_bar, self.danger_bars)
            x = threading.Thread(target=self.danger_timer_countdown)
            x.start()
        if self.is_ai:
            y = threading.Thread(target=danger_start3y)
            y.start()
        else:
            n = threading.Thread(target=dangerstart3n)
            n.start()


    #S8 --- Danger State End III Y / Danger State End III Y
    def on_s78 (self):
        if self.is_ai:
            self.dialogue.change_dialogue("Danger State End III Y") #default
            switch_danger(self.normal_bar, self.danger_bars)
            self.flashing_image.disable()
            self.assistedmode_button.disable()
            self.normalmode_button.enable()
        else:
            self.dialogue.change_dialogue("Danger State End III N") #default
            self.flashing_image.disable()
            switch_danger(self.normal_bar, self.danger_bars) 


    #S9 --- End
    def on_s89(self):
        self.timer.stop()
        self.dialogue.change_dialogue("End") #default
        post_event("task_count", self.task_canvas.count)




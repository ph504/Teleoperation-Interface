#!/usr/bin/env python3

import rospy
import random
import numpy as np
import cv2
from playsound import playsound
import state
from tkinter import * 
from tkinter.ttk import *
from PIL import ImageTk
from axis_camera.msg import Axis
from sensor_msgs.msg import Joy
import PIL.Image
import canvas
import camera 
#from dialogue import *
#from avatar import *
from avalogue import AvalogueController

from dialogue import DialogueView, DialogueModel, dialogueview_info
from avatar import AvatarView, AvatarModel, javatar_info

from button import *
from jackalAI import *
from inspection import *
import socket
import socketserver
from flashing_image import *
from labels import *
from std_msgs.msg import Bool
import global_variables   
import sys
import subprocess
from userAI import *
from bar_canvas import *
import pygame

csv_dialogue_s = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/s.csv"
csv_dialogue_ns = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/ns.csv"


csv_idle = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/IdleAvatars.csv"
csv_talking = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/TalkingAvatars.csv"
csv_reactive = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/ReactiveAvatars.csv"


def init():
    
    if len(sys.argv) != 4 and len(sys.argv) != 3:
        print("Argument length:" + str(len(sys.argv)))
        print("Usage: python3 main.py tutorial 0/1(practice mode or not) n(number of mistakes)")
        print("Usage: python3 main.py p[0:infinite] social/nonsocial")
        sys.exit(1)

    if len(sys.argv) == 4:
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]
        arg3 = sys.argv[3]
        
        if arg1 == "t":
            global_variables.tutorial_mode = True
            
        else:
            global_variables.tutorial_mode = False
            EventManager.post_event("freeze", -1) # type: ignore
            sys.exit(1)
        
        if arg2 == "s":
            global_variables.social_mode = True
        elif arg2 == "ns":
             global_variables.social_mode = False
        elif arg2 == "nn":
            global_variables.social_mode = None
            global_variables.practice_mode = False
        else:
            print("Incorrect command or typo")
            sys.exit(1)
        

        
        if arg3 == '1':
            global_variables.practice_mode = True
            EventManager.post_event("freeze", -1) # type: ignore
        elif arg3 == '0':
            global_variables.practice_mode = False
            EventManager.post_event("unfreeze", -1) # type: ignore
        else:
            print("Incorrect command or typo")
            sys.exit(1)

    if len(sys.argv) == 3:
    
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]

        global_variables.practice_mode = False
        global_variables.tutorial_mode = False
         
        global_variables.participant = arg1
       
        if arg2 == "s":
            global_variables.social_mode = True
        elif arg2 == "ns":
            global_variables.social_mode = False
        else:
            print("Incorrect command or typo")
            sys.exit(1)

def main(): 
    
    root = Tk()

    global big_canvas_info, small_canvas_info
    global timer_canvas_info, timer_label_info
    global task_canvas_info, task_label_info
    global miss_canvas_agent_info, miss_label_agent_info, miss_canvas_operator_info, miss_label_operator_info
    global score_canvas_info, score_label_info
    global circle_canvas_info
    global big_camera_label, small_camera_label, clbr_label, flir_info, axis_info


    # root.geometry("1440x900")
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    big_camera_label = global_statics.convert_to_pixels(global_statics.big_camera_label_percent, width, height)
    small_camera_label = global_statics.convert_to_pixels(global_statics.small_camera_label_percent, width, height)
    clbr_label = global_statics.convert_to_pixels(global_statics.clbr_label_percent, width, height)
    flir_info = global_statics.convert_to_pixels(global_statics.flir_info_percent, width, height)
    axis_info = global_statics.convert_to_pixels(global_statics.axis_info_percent, width, height)
    big_canvas_info = global_statics.convert_to_pixels(global_statics.big_canvas_info_percent, width, height)
    small_canvas_info = global_statics.convert_to_pixels(global_statics.small_canvas_info_percent, width, height)
    timer_canvas_info = global_statics.convert_to_pixels(global_statics.timer_canvas_info_percent, width, height)
    timer_label_info = global_statics.convert_to_pixels(global_statics.timer_label_info_percent, width, height)
    task_canvas_info = global_statics.convert_to_pixels(global_statics.task_canvas_info_percent, width, height)
    task_label_info = global_statics.convert_to_pixels(global_statics.task_label_info_percent, width, height)
    miss_canvas_agent_info = global_statics.convert_to_pixels(global_statics.miss_canvas_agent_info_percent, width, height)
    miss_label_agent_info = global_statics.convert_to_pixels(global_statics.miss_label_agent_info_percent, width, height)
    miss_canvas_operator_info = global_statics.convert_to_pixels(global_statics.miss_canvas_operator_info_percent, width, height)
    miss_label_operator_info = global_statics.convert_to_pixels(global_statics.miss_label_operator_info_percent, width, height)
    score_canvas_info = global_statics.convert_to_pixels(global_statics.score_canvas_info_percent, width, height)
    score_label_info = global_statics.convert_to_pixels(global_statics.score_label_info_percent, width, height)
    circle_canvas_info = global_statics.convert_to_pixels(global_statics.circle_canvas_info_percent, width, height)


    # width, height = 1440, 900
    root.geometry('%dx%d+0+0' % (width, height))
    root.title("Jackal Teleoperator GUI")
    tabControl = Notebook(root)
    tab1 = Frame(tabControl)
    tab2 = Frame(tabControl)
    tabControl.add(tab1, text = "Main")
    tabControl.add(tab2, text = "Inspection")
    tabControl.place(x = 5, y = 5, width=width ,height=height)
    # TODO: uncomment, commented for debugging.
    # fake collision detector, woz style
    # x = threading.Thread(target=server_program)
    # x.start()
    
    cursor_canvas_small = CursorCanvas(tab1, small_canvas_info)
    cursor_canvas_small.disable()
    cursor_canvas_big = CursorCanvas(tab1, big_canvas_info)
    cursor_canvas_big.disable()

    if camera.camera_available():    
        rospy.init_node("viewer", anonymous= True)
        rospy.loginfo("viewer node started ...")
        #global prev_angle 
        axis = Axis()
        axis.pan = -180
        pub_axis = rospy.Publisher('/axis/cmd', Axis, queue_size=10)
        pub_axis.publish(axis)
        x = rospy.wait_for_message("/axis/state", Axis).pan
        print("Initial angle: " + str(x))
        # currentangle = rospy.wait_for_message("/axis/state", Axis).pan # might be a problem
        #TODO: make the camera tilt
        # rospy.EventManager.subscriber("/axis/cmd", Axis, change_angle, callback_args=(cursor) queue_size=1) #TODO: Fix cursor change!
        # cursor_canvases = (cursor_canvas_small, cursor_canvas_big)
        # rospy.EventManager.subscriber("/axis/cmd", Axis, callback= change_angle, callback_args= cursor_canvases, queue_size=1)


    global cs, dialogue_end
    cs = 0
    dialogue_end = 0

    widgets = widget_init(root, tab1, tab2)

    def freeze(dummy = 0):
        pub.publish(True)
    
    def unfreeze(dummy = 0):
        def x():
            print("sending data to unfreeze ...")
            time.sleep(1)
            pub.publish(False)
        _x = threading.Thread(target=x)
        _x.start()
    
    def calibrate_btn_enbl(dummy = 0):
        widgets['calibrate_button'].enable()

    def calibrate_btn_dsbl(dummy = 0):
        widgets['calibrate_button'].disable()

    pub = rospy.Publisher("freeze", Bool, queue_size=10)
    EventManager.subscribe("freeze", freeze)                            # type: ignore
    EventManager.subscribe("unfreeze", unfreeze)                        # type: ignore
    EventManager.subscribe("activate_calibration", calibrate_btn_enbl)  # type: ignore
    EventManager.subscribe("calibrate_pause", calibrate_btn_dsbl)       # type: ignore
    
    EventManager.subscribe("toggle_bar", toggle_barcontroller)          # type: ignore
   
    if global_variables.tutorial_mode and not global_variables.practice_mode:
        unfreeze()
    
    
    def tab_checker():
        # what happens if neither of the values? why cant I just put ==1 in the equation
        if tabControl.index("current") == 1:
            global_variables.in_inspection = True
        elif tabControl.index("current") == 0:
            global_variables.in_inspection = False
        Tk.after(root, 100, tab_checker)
    
    tab_checker()
    
    # rospy.Subscriber("joy", Joy, callback= joy_config, callback_args= widgets)
    
    inspection_page = InspectionPage(tab2, widgets['task_canvas'])
    if not global_variables.tutorial_mode:
        gui_fsm = state.TeleopGUIMachine(widgets['timer_canvas'], widgets['avalogue'], widgets['dialogue_text'], widgets['manual_button'], widgets['auto_button'], jackal_avatar= None, flashing_image=widgets['flashing_image'], tsk_cnvs=widgets['task_canvas'], cmr_frm = widgets['view_front'], jckl_ai= widgets['jackal_ai'], cntdwn= widgets['countdown'])
        
    else:
        tutorial_fsm = state.TutorialGUIMachine(timer= widgets['timer_canvas'], amode_btn=widgets['auto_button'], flashing_image= widgets['flashing_image'], jckl_ai= widgets['jackal_ai'], nmode_btn= widgets['manual_button'], avalogue= widgets['avalogue'])

    #if not global_variables.tutorial_mode: start_button.add_event(gui_fsm.s01)
    #if not global_variables.tutorial_mode: yes_button.add_event(gui_fsm.on_yes)
    #if not global_variables.tutorial_mode: no_button.add_event(gui_fsm.on_no)
    if not global_variables.tutorial_mode: 
        widgets['task_canvas'].add_fsm(gui_fsm)
    else:
        widgets['task_canvas'].add_fsm(tutorial_fsm)


    if not global_variables.tutorial_mode: 
        widgets['timer_canvas'].add_fsm(gui_fsm)
    else:
        widgets['timer_canvas'].add_fsm(tutorial_fsm)


    if not global_variables.tutorial_mode: widgets['countdown'].add_fsm(gui_fsm)

    widgets['calibrate_button'].add_event(widgets['calibrate_label'].activate)
    
    #if  global_variables.tutorial_mode: auto_button.enable()

    if global_variables.tutorial_mode: 
        bind_keyboard(root, cursor_canvas_small, cursor_canvas_big, widgets['task_canvas'], widgets['view_back'], widgets['view_front'], widgets['manual_button'], widgets['auto_button'], widgets['circle_canvas'], widgets['jackal_ai'], tutorial_fsm)
        # bind_keyboard(root, cursor_canvas_small, cursor_canvas_big, task_canvas, view_back, view_front, manual_button, auto_button, circle_canvas, jackal_ai, tutorial_fsm)

    
    if camera.camera_available():
        print('***Arya*** Camera Available.')
        try:
            tab1.mainloop()
        except rospy.ROSInterruptException:
            pass
    else:     
        print('***Arya*** Camera Unavailable.')
        tab1.mainloop()

def camera_widget(root, tab1, tab2):
    pass
#############################################################################

#############################################################################
def widget_init(root, tab1, tab2):

    print('***Arya*** Initializing Widgets ...')
    widgets = {}

    def initialize_camera_views():
        widgets['view_back'] = camera.CameraView(tab1, flir_info, camera.camera_available(), "flir")
        widgets['view_front'] = camera.CameraView(tab1, axis_info, camera.camera_available(), "axis")

    def initialize_buttons():
        widgets['manual_button'] = BaseButton(root, button_manual_info, enable=False)
        widgets['auto_button'] = BaseButton(root, button_auto_info, enable=False)
        widgets['calibrate_button'] = BaseButton(root, button_calibrate_info, activate=True, enable=False)

    def initialize_canvases():
        widgets['countdown'] = CountdownCanvas(root, countdown_info)
        widgets['timer_canvas'] = TimerCanvas(root, timer_canvas_info)
        widgets['task_canvas'] = TaskCanvas(root, task_canvas_info)
        widgets['circle_canvas'] = CircleCanvas(tab2, circle_canvas_info) if not global_variables.practice_mode else None
        widgets['score_canvas'] = None

    def initialize_labels():
        widgets['small_label'] = CameraLabel(tab1, small_camera_label, "Back Camera")
        widgets['big_label'] = CameraLabel(tab1, big_camera_label, "Front Camera")
        widgets['calibrate_label'] = CalibrateLabel(root, clbr_label, "")

        timer_label = Label(root, text="Timer", font=timer_label_info["font"], fg=timer_label_info["color"])
        timer_label.place(x = timer_label_info["x"], y = timer_label_info["y"], width=timer_label_info["width"], height=timer_label_info["height"])
        miss_label_operator = Label(root, text="Operator", font=miss_label_operator_info["font"], fg=miss_label_operator_info["color"])
        miss_label_operator.place(x = miss_label_operator_info["x"], y = miss_label_operator_info["y"], width=miss_label_operator_info["width"], height=miss_label_operator_info["height"])
        miss_label_agent = Label(root, text="Agent", font=miss_label_agent_info["font"], fg=miss_label_agent_info["color"])
        miss_label_agent.place(x = miss_label_agent_info["x"], y = miss_label_agent_info["y"], width=miss_label_agent_info["width"], height=miss_label_agent_info["height"])
        task_label = Label(root, text="Task", font=task_label_info["font"], fg=task_label_info["color"])
        task_label.place(x = task_label_info["x"], y = task_label_info["y"], width=task_label_info["width"], height=task_label_info["height"])
        
    def initialize_dialogue_system():
        if not global_variables.tutorial_mode or global_variables.practice_mode:
            widgets['dialogue_view'] = DialogueView(root, dialogueview_info)
            widgets['dialogue_model'] = DialogueModel(root, csv_dialogue_ns if not global_variables.social_mode else csv_dialogue_s)
            widgets['avatar_view'] = AvatarView(root, javatar_info, global_variables.social_mode)
            widgets['avatar_model'] = AvatarModel(csv_idle, csv_talking, csv_reactive)

            widgets['avalogue'] = AvalogueController(root, widgets['dialogue_model'], widgets['dialogue_view'], widgets['avatar_model'], widgets['avatar_view'])

            if not global_variables.tutorial_mode:
                widgets['avalogue'].set_avalogue("t_default", "start_q")
            else:
                widgets['avalogue'].set_avalogue("t_default", "t_start_q")
        else:
            widgets['avatar_view'] = None
            widgets['avatar_model'] = None
            widgets['avalogue'] = None
            widgets['dialogue_view'] = None
            widgets['dialogue_model'] = None
        widgets['dialogue_text'] = None

    def initialize_misc_components():
        widgets['miss_canvas_operator'] = MissCanavas(root, miss_canvas_operator_info, "operator")
        widgets['miss_canvas_agent'] = MissCanavas(root, miss_canvas_agent_info, "agent")
        widgets['flashing_image'] = FlashingImage(root, flashing_image_info)


    def initialize_ai():
        widgets['jackal_ai'] = JackalAI(root)
        widgets['user_ai'] = UserAI(root)

    # Call the modularized initialization functions
    initialize_camera_views()
    initialize_buttons()
    initialize_canvases()
    initialize_labels()
    initialize_dialogue_system()
    initialize_misc_components()
    initialize_ai()

    return widgets
#############################################################################

#############################################################################
def bind_keyboard(tab1, cursor_canvas_small, cursor_canvas_big, task_canvas, view_back, view_front, manual_button, auto_button, circle_canvas, jackal_ai, tutorial_fsm):
# def bind_keyboard(tab1, cursor_canvas_small, cursor_canvas_big, task_canvas, view_back, view_front, manual_button, auto_button, circle_canvas, jackal_ai, tutorial_fsm):
    
    if not global_variables.practice_mode:
        tab1.bind('s', lambda e: switch(back = view_back, front = view_front, small=cursor_canvas_small, big=cursor_canvas_big))
        tab1.bind('o', lambda e: task_canvas.plus()) 
        tab1.bind('[', lambda e: color_transition(view_back, view_front, circle_canvas))
        tab1.bind(']', lambda e: color_transition_reverse(view_back, view_front, circle_canvas))
        tab1.bind('b', lambda e: toggle_barcontroller())
        tab1.bind('a', lambda e: toggle_assistedmode(jackal_ai,manual_button,auto_button))
        tab1.bind('x', lambda e: pygame.mixer.find_channel().play(global_variables.beep_sound))
        tab1.bind('z', lambda e: pygame.mixer.find_channel().play(global_variables.beep_sound))
        
    elif global_variables.practice_mode:
        tab1.bind('9', lambda e: start_tutorial(tab1, tutorial_fsm))
        tab1.bind('x', lambda e: playsound_beep_thread())
        tab1.bind('z', lambda e: playsound_beep_thread())
        
        
    
def color_transition(view_b, view_f,circle_canvas):
    view_b.color_transition()
    view_f.color_transition()
    circle_canvas.color_transition()
    
def start_tutorial(tab, t_fsm):
    tab.unbind_all('s')
    tab.unbind_all('w')
    tab.unbind_all('`')
    tab.unbind_all('1')
    tab.unbind_all('2')
    tab.unbind_all('3')
    tab.unbind_all('o') 
    tab.unbind_all('[')
    tab.unbind_all(']')
    tab.unbind_all('b')
    tab.unbind_all('a')
    tab.unbind_all('9')
    t_fsm.s01()

def color_transition_reverse(view_b, view_f, circle_canvas):
    view_b.color_transition_reverse()
    view_f.color_transition_reverse()
    circle_canvas.color_transition_reverse()

def toggle_assistedmode(jackal_ai, man_btn, ato_btn):
    
    if global_variables.jackalai_active:
        jackal_ai.disable()
        man_btn.enable()
        ato_btn.disable()
        
    else:
        jackal_ai.enable()
        man_btn.disable()
        ato_btn.enable()
    
def toggle_barcontroller():
    global_variables.bar_controller = not global_variables.bar_controller
    EventManager.post_event("start_move_bars", -1) # type: ignore

def change_scan_mode():
    camera.CameraView.scan_mode = not camera.CameraView.scan_mode
    print(camera.CameraView.scan_mode)

def switch(back, front, small, big):
        
        EventManager.post_event("label_camera_switch", -1) # type: ignore
        
        if back.is_front == False:
            #Flir is front, Axis is back
            front.update_pos(global_statics.flir_info)
            back.update_pos(global_statics.axis_info)
            #small.switch_camera()
            #big.switch_camera()
        else:
            #Axis is front, Flir is back
            front.update_pos(global_statics.axis_info)
            back.update_pos(global_statics.flir_info)
            #small.switch_camera()
            #big.switch_camera()
       
def switch_auto(auto_button, manual_button):

    if auto_button.active:
        auto_button.disable()
        manual_button.enable()
    elif manual_button.active:
        auto_button.enable()
        manual_button.disable()

def server_program():
    socketserver.TCPServer.allow_reuse_address = True

    # collision detector device
    HOST = '192.168.2.191'
    PORT = 4001

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST, PORT))
                s.listen()
                s.settimeout(None)
                conn, addr = s.accept()
                with conn:
                    print(f"Connected by {addr}")
                    while True:
                        try:
                            data = conn.recv(1024)
                            data = data.decode('utf-8')
                            if not data:
                                break
                            ack = "ACK"
                            conn.send(ack.encode('utf-8'))
                        except socket.timeout:
                                print("timeout error!!!!")
                                break
                    
                        print("From connected user: " + data)
                        if int(data) == 0:
                            Logger.log("calibration", 1) # type: ignore
                            EventManager.post_event("activate_calibration", -1) # type: ignore
                        else:
                            Logger.log("collision", data) # type: ignore
                            EventManager.post_event("collision", data) # type: ignore
            
            except Exception as e:
                print("shit happened: " + str(e))  
                break      
    
def change_angle(data, canvases):
    global prev_angle
    if data.pan - prev_angle >= 1:
        canvases[0].rotate("right")
        canvases[1].rotate("right")
    elif data.pan - prev_angle <= -1:
        canvases[0].rotate("left")
        canvases[1].rotate("left")
 
    
    prev_angle = data.pan

def joy_config(data, widgets):
    global rb1, rb2normal, rb3, cs, dialogue_end

    jackal_ai = widgets["jackal_ai"]

    if global_variables.in_inspection:
        return

    #camera switch
    cs_buff = cs
    cs = data.buttons[3]
    if cs == 1 and cs_buff == 0:
        switch(back = widgets["view_back"], front = widgets["view_front"], small=widgets["small_label"], big=widgets["big_label"])

    #end the dialogue talking sound and show all the text
    dialogue_end_buff = dialogue_end
    dialogue_end = data.buttons[5]
    if dialogue_end == 1 and dialogue_end_buff == 0:
        EventManager.post_event("stop_talking", 1) # type: ignore

def playsound_beep_thread():
    x = threading.Thread(target=playsound("/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/sounds/beep.wav"))   
    x.start()

def playsound_animalese_thread():
    x = threading.Thread(target=playsound(random.choice(global_variables.animalese_sound_dir)))
    x.start

if __name__ == "__main__":
    init()
    main()
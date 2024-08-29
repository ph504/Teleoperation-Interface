#!/usr/bin/env python3

import rospy
import numpy as np
import cv2
from playsound import playsound
from state import *
from tkinter import * 
from tkinter.ttk import *
from PIL import ImageTk
from axis_camera.msg import Axis
from sensor_msgs.msg import Joy
import PIL.Image
from canvas import *
from camera import * 
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
            EventManager.post_event("freeze", -1)
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
    root.geometry("1440x900")
    # width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    # root.geometry('%dx%d+0+0' % (width,height))
    root.title("Jackal Teleoperator GUI")
    tabControl = Notebook(root)
    tab1 = Frame(tabControl)
    tab2 = Frame(tabControl)
    tabControl.add(tab1, text = "Main")
    tabControl.add(tab2, text = "Inspection")
    tabControl.place(x = 5, y = 5, width= 1440 ,height= 900)
    
    # TODO: uncomment, commented for debugging.
    # fake collision detector, woz style
    # x = threading.Thread(target=server_program)
    # x.start()

    
    cursor_canvas_small = CursorCanvas(tab1, small_canvas_info)
    cursor_canvas_small.disable()
    cursor_canvas_big = CursorCanvas(tab1, big_canvas_info)
    cursor_canvas_big.disable()

    if camera_available:    
        rospy.init_node("viewer", anonymous= True)
        rospy.loginfo("viewer node started ...")
        #global prev_angle 
        axis = Axis()
        axis.pan = -180
        pub_axis = rospy.Publisher('/axis/cmd', Axis, queue_size=10)
        pub_axis.publish(axis)
        x = rospy.wait_for_message("/axis/state", Axis).pan
        print("Initial angle: " + str(x))
        currentangle = rospy.wait_for_message("/axis/state", Axis).pan # might be a problem
        #TODO: make the camera tilt
        #rospy.EventManager.subscriber("/axis/cmd", Axis, change_angle, callback_args=(cursor) queue_size=1) #TODO: Fix cursor change!
        #cursor_canvases = (cursor_canvas_small, cursor_canvas_big)
        #rospy.EventManager.subscriber("/axis/cmd", Axis, callback= change_angle, callback_args= cursor_canvases, queue_size=1)


    global rb1, rb2normal, rb3, cs, dialogue_end
    rb1 = 0 
    rb2normal = 0
    rb3 = 0
    cs = 0
    dialogue_end = 0

    (bar_canvas, 
    danger_canvases, 
    task_canvas, 
    view_back, 
    view_front,
    manual_button,
    auto_button,
    a_model,
    a_view,
    dialogue_model,
    dialogue_view,
    avalogue,
    dialogue_text,
    timer_canvas,
    score_canvas,
    flashing_image,
    circle_canvas,
    jackal_ai,
    small_label,
    big_label,
    calibrate_button,
    calibrate_lbl,
    countdown) = widget_init(root, tab1, tab2)


    widgets = {
        "small_label": small_label,
        "big_label": big_label,
        "bar_canvas": bar_canvas,
        "danger_canvases": danger_canvases,
        "task_canvas": task_canvas,
        "view_back": view_back,
        "view_front": view_front,
        "dialogue_text": dialogue_text,
        "jackal_ai": jackal_ai
    }

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
        calibrate_button.enable()

    def calibrate_btn_dsbl(dummy = 0):
        calibrate_button.disable()

    pub = rospy.Publisher("freeze", Bool, queue_size=10)
    EventManager.subscribe("freeze", freeze)
    EventManager.subscribe("unfreeze", unfreeze) # type: ignore
    EventManager.subscribe("activate_calibration", calibrate_btn_enbl)
    EventManager.subscribe("calibrate_pause", calibrate_btn_dsbl)
    
    EventManager.subscribe("toggle_bar", toggle_barcontroller)
   
    if global_variables.tutorial_mode and not global_variables.practice_mode:
        unfreeze()
    
    
    def tab_checker():
        if tabControl.index("current") == 1:
            global_variables.in_inspection = True
        elif tabControl.index("current") == 0:
            global_variables.in_inspection = False
        Tk.after(root, 100, tab_checker)
    
    tab_checker()
    
    # # rospy.Subscriber("joy", Joy, callback= joy_config, callback_args= widgets)
    
    # inspection_page = InspectionPage(tab2, task_canvas)
    # if not global_variables.tutorial_mode:
    #     gui_sfm = TeleopGUIMachine(timer_canvas, avalogue, dialogue_text, manual_button, auto_button, bar_canvas, danger_canvases, jackal_avatar= None, flashing_image=flashing_image, tsk_cnvs=task_canvas, cmr_frm = view_front, jckl_ai= jackal_ai, cntdwn= countdown)
    # else:
    #     tutorial_fsm = TutorialGUIMachine(timer= timer_canvas, amode_btn=auto_button, d_bars= danger_canvases, flashing_image= flashing_image, jckl_ai= jackal_ai, n_bar= bar_canvas, nmode_btn= manual_button, avalogue= avalogue)
    

    # #if not global_variables.tutorial_mode: start_button.add_event(gui_sfm.s01)
    # #if not global_variables.tutorial_mode: yes_button.add_event(gui_sfm.on_yes)
    # #if not global_variables.tutorial_mode: no_button.add_event(gui_sfm.on_no)
    # if not global_variables.tutorial_mode: 
    #     task_canvas.add_fsm(gui_sfm)
    # else:
    #     task_canvas.add_fsm(tutorial_fsm)


    # if not global_variables.tutorial_mode: 
    #     timer_canvas.add_fsm(gui_sfm)
    # else:
    #     timer_canvas.add_fsm(tutorial_fsm)


    # if not global_variables.tutorial_mode: countdown.add_fsm(gui_sfm)

    # calibrate_button.add_event(calibrate_lbl.activate)
    
    # #if  global_variables.tutorial_mode: auto_button.enable()

    # if global_variables.tutorial_mode: 
    #     bind_keyboard(root, cursor_canvas_small, cursor_canvas_big, bar_canvas, danger_canvases, task_canvas, view_back, view_front, manual_button, auto_button, circle_canvas, jackal_ai, tutorial_fsm)
    

    if camera_available:
        try:
            tab1.mainloop()
        except rospy.ROSInterruptException:
            pass
    else:     
        tab1.mainloop()

def widget_init(root, tab1, tab2):
    bar_canvas = BarCanvas(tab1, bar_canvas_info_main, danger= False)
    #if global_variables.tutorial_mode: bar_canvas.start()
    # danger_canvases = (BarCanvas(tab1, bar_canvas_info1,danger= True),
    #                        BarCanvas(tab1,bar_canvas_info2, danger= True),
    #                          BarCanvas(tab1,bar_canvas_info3, danger = True))


    dialogue_text = None
    

    if not global_variables.tutorial_mode or global_variables.practice_mode:
        
        dialogue_view = DialogueView(root, dialogueview_info)
        dialogue_model = None
        if not global_variables.social_mode:
            dialogue_model = DialogueModel(root, csv_dialogue_ns)
        else:
            dialogue_model = DialogueModel(root, csv_dialogue_s)
            
        avatar_view = AvatarView(root, javatar_info, global_variables.social_mode)
        avatar_model = AvatarModel(csv_idle, csv_talking, csv_reactive)

        avalogue = AvalogueController(root, dialogue_model, dialogue_view, avatar_model, avatar_view)
        
        if not global_variables.tutorial_mode:
            avalogue.set_avalogue("t_default","start_q")
        else:
            avalogue.set_avalogue("t_default","t_start_q")

    else:
        avatar_view = None
        avatar_model = None
        avalogue = None
        dialogue_view = None
        dialogue_model = None


    
    user_ai = UserAI(root)
    view_back = CameraView(tab1, flir_info, camera_available, "flir")
    view_front = CameraView(tab1, axis_info, camera_available, "axis")
    manual_button = BaseButton(root, button_manual_info, enable = False)
    auto_button = BaseButton(root, button_auto_info, enable= False)
    countdown = CountdownCanvas(root, countdown_info)
   
    #yes_button = BaseButton(root, button_yes_info, activate=False, enable=False)
    #no_button = BaseButton(root, button_no_info, activate = False, enable=False)
    #if not global_variables.tutorial_mode:
     #   start_button = BaseButton(root, button_start_info, activate=True, enable=False)
    #else: start_button = None
    
    if global_variables.tutorial_mode and global_variables.practice_mode == False:
        freeze_button = BaseButton(root, button_freeze_info, activate=True, enable=False)
    else:
        freeze_button = BaseButton(root, button_freeze_info, activate=True, enable=True)

    calibrate_button = BaseButton(root, button_calibrate_info, activate=True, enable=False)

    timer_canvas = TimerCanvas(root, timer_canvas_info)
    timer_lbl = Label(root, text="Timer", font=timer_lbl_info["font"], fg=timer_lbl_info["color"])
    timer_lbl.place(x = timer_lbl_info["x"], y = timer_lbl_info["y"], width=timer_lbl_info["width"], height=timer_lbl_info["height"])

    small_label = CameraLabel(tab1, small_cmr_lbl, "Back Camera")
    big_label = CameraLabel(tab1, big_cmr_lbl, "Front Camera")
    calibrate_lbl = CalibrateLabel(root, clbr_lbl, "")
    

    score_canvas = None
    #score_canvas = ScoreCanvas(root, score_canvas_info)
    #score_lbl = Label(root, text="Score", font=score_lbl_info["font"], fg=score_lbl_info["color"])
    #score_lbl.place(x = score_lbl_info["x"], y = score_lbl_info["y"], width=score_lbl_info["width"], height=score_lbl_info["height"])
    
    
    if not global_variables.practice_mode: circle_canvas = CircleCanvas(tab2, circle_canvas_info)
    else: circle_canvas = None
    
    miss_canvas_operator = MissCanavas(root,miss_canvas_operator_info, "operator")
    miss_lbl_operator = Label(root, text="Operator", font=miss_lbl_operator_info["font"], fg=miss_lbl_operator_info["color"])
    miss_lbl_operator.place(x = miss_lbl_operator_info["x"], y = miss_lbl_operator_info["y"], width=miss_lbl_operator_info["width"], height=miss_lbl_operator_info["height"])
    
    miss_canvas_agent = MissCanavas(root,miss_canvas_agent_info, "agent")
    miss_lbl_agent = Label(root, text="Agent", font=miss_lbl_agent_info["font"], fg=miss_lbl_agent_info["color"])
    miss_lbl_agent.place(x = miss_lbl_agent_info["x"], y = miss_lbl_agent_info["y"], width=miss_lbl_agent_info["width"], height=miss_lbl_agent_info["height"])

    task_canvas = TaskCanvas(root, task_canvas_info)
    task_lbl = Label(root, text="Task", font=task_lbl_info["font"], fg=task_lbl_info["color"])
    task_lbl.place(x = task_lbl_info["x"], y = task_lbl_info["y"], width=task_lbl_info["width"], height=task_lbl_info["height"])

    flashing_image = FlashingImage(root, flashing_image_info)

    jackal_ai = JackalAI(root)
    
    return (bar_canvas,
            # danger_canvases,
            task_canvas,
            view_back,
            view_front,
            manual_button,
            auto_button,
            avatar_model, 
            avatar_view, 
            dialogue_model, 
            dialogue_view, 
            avalogue, 
            dialogue_text, 
            timer_canvas, 
            score_canvas, 
            flashing_image, 
            circle_canvas, 
            jackal_ai, 
            small_label, 
            big_label, 
            calibrate_button, 
            calibrate_lbl, 
            countdown)

def bind_keyboard(tab1, cursor_canvas_small, cursor_canvas_big, bar_canvas, danger_canvases, task_canvas, view_back, view_front, manual_button, auto_button, circle_canvas, jackal_ai, tutorial_fsm):
    
    if not global_variables.practice_mode:
        tab1.bind('s', lambda e: switch(back = view_back, front = view_front, small=cursor_canvas_small, big=cursor_canvas_big))
        tab1.bind('w', lambda e: switch_danger(bar_canvas, danger_canvases))
        tab1.bind('`', lambda e: bar_canvas.user_reset())
        tab1.bind('1', lambda e: danger_canvases[0].user_reset())
        tab1.bind('2', lambda e: danger_canvases[1].user_reset())
        tab1.bind('3', lambda e: danger_canvases[2].user_reset())
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
    EventManager.post_event("start_move_bars", -1)

def change_scan_mode():
    CameraView.scan_mode = not CameraView.scan_mode
    print(CameraView.scan_mode)

def switch(back, front, small, big):
        
        EventManager.post_event("label_camera_switch", -1)
        
        if back.is_front == False:
            #Flir is front, Axis is back
            front.update_pos(flir_info)
            back.update_pos(axis_info)
            #small.switch_camera()
            #big.switch_camera()
        else:
            #Axis is front, Flir is back
            front.update_pos(axis_info)
            back.update_pos(flir_info)
            #small.switch_camera()
            #big.switch_camera()

def switch_danger(barcanvas, dangercanvases):
    if barcanvas.active:
        barcanvas.reset_bar()
        barcanvas.disable()
        for dangercanvas in dangercanvases:
            dangercanvas.reset_bar()
        for dangercanvas in dangercanvases:
            dangercanvas.enable()
            dangercanvas.start()
        BarCanvas.danger_mode = True
        global_variables.danger_mode = True
    else:
        barcanvas.reset_bar()
        barcanvas.enable()
        for dangercanvas in dangercanvases:
            dangercanvas.reset_bar() 
        for dangercanvas in dangercanvases:
            dangercanvas.disable() 
        BarCanvas.danger_mode = False
        global_variables.danger_mode = False
       
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
                            Logger.log("calibration", 1)
                            EventManager.post_event("activate_calibration", -1) # type: ignore
                        else:
                            Logger.log("collision", data)
                            EventManager.post_event("collision", data)
            
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
    
    #reset bar 1
    rb1_buff = rb1
    rb1 = data.buttons[2]
    if rb1 == 1 and rb1_buff == 0:
         if BarCanvas.danger_mode:
            if not global_variables.jackalai_active:
                widgets["danger_canvases"][0].user_reset()
          

    #reset bar 2 and normal
    rb2normal_buff = rb2normal
    rb2normal = data.buttons[1] 
    
    if rb2normal == 1 and rb2normal_buff == 0:
        if BarCanvas.danger_mode:
            if not global_variables.jackalai_active:
               widgets["danger_canvases"][1].user_reset()
            
        else:
            widgets["bar_canvas"].user_reset()
            
   
    #reset bar 3
    rb3_buff = rb3
    rb3 = data.buttons[0]
    if rb3 == 1 and rb3_buff == 0:
         if BarCanvas.danger_mode:
            if not global_variables.jackalai_active:
                widgets["danger_canvases"][2].user_reset()
            


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

if __name__ == "__main__":
    init()
    main()
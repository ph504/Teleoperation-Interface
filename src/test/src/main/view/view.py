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
from avatar import *
from dialogue import *
from button import *
from jackalAI import *
from inspection import *
import socket
import socketserver
from flashing_image import *
from labels import *
    

tutorial_mode = False

def main():
       
    root = Tk()
    root.geometry("1920x1080")
    root.title("Jackal Teleoperator GUI")
    
    tabControl = Notebook(root)
    tab1 = Frame(tabControl)
    tab2 = Frame(tabControl)
    tabControl.add(tab1, text = "Main")
    tabControl.add(tab2, text = "Inspection")
    tabControl.place(x = 5, y = 5, width= 1920 ,height= 1080)
    

    x = threading.Thread(target=server_program)
    x.start()

    if not tutorial_mode: jackal = Avatar(root, javatar_info,javatar_images)
    
    cursor_canvas_small = CursorCanvas(tab1, small_canvas_info)
    cursor_canvas_small.disable()
    cursor_canvas_big = CursorCanvas(tab1, big_canvas_info)
    cursor_canvas_big.disable()

   
    

    


    if camera_available == True:    
        rospy.init_node("viewer", anonymous= True)
        rospy.loginfo("viewer node started ...")
        #global prev_angle 
        axis = Axis()
        axis.pan = -180
        pub_axis = rospy.Publisher('/axis/cmd', Axis, queue_size=10)
        pub_axis.publish(axis)
        x = rospy.wait_for_message("/axis/state", Axis).pan
        print("Initial angle: " + str(x))
        #currentangle = rospy.wait_for_message("/axis/state", Axis).pan # might be a problem
        #TODO: make the camera tilt
        #rospy.Subscriber("/axis/cmd", Axis, change_angle, callback_args=(cursor) queue_size=1) #TODO: Fix cursor change!
        #cursor_canvases = (cursor_canvas_small, cursor_canvas_big)
        #rospy.Subscriber("/axis/cmd", Axis, callback= change_angle, callback_args= cursor_canvases, queue_size=1)


    global rb1, rb2normal, rb3, cs, dialogue_end
    rb1 = 0 
    rb2normal = 0
    rb3 = 0
    cs = 0
    dialogue_end = 0




    bar_canvas, danger_canvases, task_canvas, view_back, view_front, manual_button, auto_button, dialogue_text, yes_button, no_button, timer_canvas, start_button, score_canvas, flashing_image, circle_canvas, jackal_ai, small_lbl, big_lbl = widget_init(root, tab1, tutorial_mode)

    widgets = {
        "small_label": small_lbl,
        "big_label": big_lbl,
        "bar_canvas": bar_canvas,
        "danger_canvases": danger_canvases,
        "task_canvas": task_canvas,
        "view_back": view_back,
        "view_front": view_front,
        "dialogue_text": dialogue_text,
        "jackal_ai": jackal_ai
    }
    rospy.Subscriber("joy", Joy, callback= joy_config, callback_args= widgets)
    
    inspection_page = InspectionPage(tab2, task_canvas)
    if not tutorial_mode:
        gui_sfm = TeleopGUIMachine(timer_canvas, dialogue_text, start_button, yes_button, no_button, manual_button, auto_button, bar_canvas, danger_canvases, jackal_avatar= jackal, flashing_image=flashing_image, tsk_cnvs=task_canvas, circle_cnvs= circle_canvas, jckl_ai= jackal_ai)
    

    if not tutorial_mode: start_button.add_event(gui_sfm.s01)
    if not tutorial_mode: yes_button.add_event(gui_sfm.on_yes)
    if not tutorial_mode: no_button.add_event(gui_sfm.on_no)
    if not tutorial_mode: task_canvas.add_fsm(gui_sfm)
    if not tutorial_mode: timer_canvas.add_fsm(gui_sfm)


    
    if tutorial_mode: 
        bind_keyboard(root, cursor_canvas_small, cursor_canvas_big, bar_canvas, danger_canvases, task_canvas, view_back, view_front, manual_button, auto_button,circle_canvas)
    

    if camera_available == True:
        try:
            tab1.mainloop()
        except rospy.ROSInterruptException:
            pass
    else:
            tab1.mainloop()

def widget_init(root, tab1, tutorial_mode):
    bar_canvas = BarCanvas(tab1, bar_canvas_info_main, danger= False)
    if tutorial_mode: bar_canvas.start()
    danger_canvases = (BarCanvas(tab1, bar_canvas_info1,danger= True),
                           BarCanvas(tab1,bar_canvas_info2, danger= True),
                             BarCanvas(tab1,bar_canvas_info3, danger = True))
    if not tutorial_mode: dialogue_text = DialogueBox(root, dbox_info, social_dialogue_dict)
    else: dialogue_text = None
    
    view_back = CameraView(tab1, flir_info, camera_available, "flir")
    view_front = CameraView(tab1, axis_info, camera_available, "axis")
    manual_button = BaseButton(root, button_manual_info, enable = False)
    auto_button = BaseButton(root, button_auto_info, enable= False)

    yes_button = BaseButton(root, button_yes_info, activate=False, enable=False)
    no_button = BaseButton(root, button_no_info, activate = False, enable=False)
    if not tutorial_mode: start_button = BaseButton(root, button_start_info, activate=True, enable=False)
    else: start_button = None
    
    timer_canvas = TimerCanvas(root, timer_canvas_info)
    timer_lbl = Label(root, text="Timer", font=timer_lbl_info["font"], fg=timer_lbl_info["color"])
    timer_lbl.place(x = timer_lbl_info["x"], y = timer_lbl_info["y"], width=timer_lbl_info["width"], height=timer_lbl_info["height"])

    small_lbl = CameraLabel(tab1, small_cmr_lbl, "Back Camera")
    big_lbl = CameraLabel(tab1, big_cmr_lbl, "Front Camera")

    score_canvas = None
    #score_canvas = ScoreCanvas(root, score_canvas_info)
    #score_lbl = Label(root, text="Score", font=score_lbl_info["font"], fg=score_lbl_info["color"])
    #score_lbl.place(x = score_lbl_info["x"], y = score_lbl_info["y"], width=score_lbl_info["width"], height=score_lbl_info["height"])
    
    
    circle_canvas = CircleCanvas(root, circle_canvas_info)

    task_canvas = TaskCanvas(root, task_canvas_info)
    task_lbl = Label(root, text="Task", font=task_lbl_info["font"], fg=task_lbl_info["color"])
    task_lbl.place(x = task_lbl_info["x"], y = task_lbl_info["y"], width=task_lbl_info["width"], height=task_lbl_info["height"])

    flashing_image = FlashingImage(root, flashing_image_info)

    jackal_ai = JackalAI()
    
    return bar_canvas,danger_canvases,task_canvas,view_back,view_front,manual_button,auto_button, dialogue_text, yes_button, no_button, timer_canvas, start_button, score_canvas, flashing_image, circle_canvas, jackal_ai, small_lbl, big_lbl

def bind_keyboard(tab1, cursor_canvas_small, cursor_canvas_big, bar_canvas, danger_canvases, task_canvas, view_back, view_front, manual_button, auto_button, circle_canvas):
    
    tab1.bind('s', lambda e: switch(back = view_back, front = view_front, small=cursor_canvas_small, big=cursor_canvas_big))
    tab1.bind('w', lambda e: switch_danger(bar_canvas, danger_canvases))
    tab1.bind('`', lambda e: reset_bar(bar_canvas))
    tab1.bind('1', lambda e: reset_bar(danger_canvases[0]))
    tab1.bind('2', lambda e: reset_bar(danger_canvases[1]))
    tab1.bind('3', lambda e: reset_bar(danger_canvases[2]))
    tab1.bind('o', lambda e: task_canvas.plus()) 
    tab1.bind('0', lambda e: circle_canvas.color_transition())

def change_scan_mode():
    CameraView.scan_mode = not CameraView.scan_mode
    print(CameraView.scan_mode)

def switch(back, front, small, big):
        print("the switch is happening!")

        if back.is_front == False:
            #Flir is front ,Axis is back
            front.update_pos(flir_info)
            back.update_pos(axis_info)
            small.switch_camera()
            big.switch_camera()
            
            #small.enable()
            #big.disable()
        else:
            #Axis is front,Flir is back
            front.update_pos(axis_info)
            back.update_pos(flir_info)
            small.switch_camera()
            big.switch_camera()
            #small.disable()
            #big.enable()

def reset_bar(bar):
    bar.reset_button()

def switch_danger(barcanvas, dangercanvases):
    if barcanvas.active:
        barcanvas.reset()
        barcanvas.disable()
        for dangercanvas in dangercanvases:
            dangercanvas.reset() 
        for dangercanvas in dangercanvases:
            dangercanvas.enable()
            dangercanvas.start()
        BarCanvas.danger_mode = True
    else:
        barcanvas.reset()
        barcanvas.enable()
        for dangercanvas in dangercanvases:
            dangercanvas.reset() 
        for dangercanvas in dangercanvases:
            dangercanvas.disable() 
        BarCanvas.danger_mode = False
       
def switch_auto(auto_button, manual_button):

    if auto_button.active:
        auto_button.disable()
        manual_button.enable()
    elif manual_button.active:
        auto_button.enable()
        manual_button.disable()

def server_program():
    socketserver.TCPServer.allow_reuse_address = True

    HOST = '192.168.2.15'
    PORT = 4001

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                data = data.decode('utf-8')
                if not data:
                    break
                print("From connected user: " + data)
                post_event("collision", data)
   
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

    #reset bar 1
    rb1_buff = rb1
    rb1 = data.buttons[2]
    if rb1 == 1 and rb1_buff == 0:
         if BarCanvas.danger_mode:
            if not jackal_ai.active:
                reset_bar(widgets["danger_canvases"][0])
          

    #reset bar 2 and normal
    rb2normal_buff = rb2normal
    rb2normal = data.buttons[1] 
    
    if rb2normal == 1 and rb2normal_buff == 0:
        if BarCanvas.danger_mode:
            if not jackal_ai.active:
                reset_bar(widgets["danger_canvases"][1])
            
        else:
            reset_bar(widgets["bar_canvas"])
            
   
    #reset bar 3
    rb3_buff = rb3
    rb3 = data.buttons[0]
    if rb3 == 1 and rb3_buff == 0:
         if BarCanvas.danger_mode:
            if not jackal_ai.active:
                reset_bar(widgets["danger_canvases"][2])
            


    #camera switch
    cs_buff = cs
    cs = data.buttons[3]
    if cs == 1 and cs_buff == 0:
        switch(back = widgets["view_back"], front = widgets["view_front"], small=widgets["small_label"], big=widgets["big_label"])

    #end the dialogue talking sound and show all the text
    dialogue_end_buff = dialogue_end
    dialogue_end = data.buttons[5]
    if dialogue_end == 1 and dialogue_end_buff == 0:
        post_event("stop_talking", 1)


    
 
if __name__ == "__main__":
    main()
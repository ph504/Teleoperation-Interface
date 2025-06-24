# from main.utils.path_setup import extend_path_to_root
# extend_path_to_root()
import sys
import os

# sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/')
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# print(project_root)
# print("THE FILE IS HERE", __file__)
sys.path.insert(0, project_root)

from main.utils import ros_guard as rg

if rg.HAS_ROS:
    import rospy
    import std_msgs.msg as std_msg
    import axis_camera.msg as ac_msg

import tkinter as tk
import tkinter.ttk as ttk
from playsound import playsound
from main.view import camera
from main.view import button
import inspection
from main.view import canvas
from main.view import labels
from main.data import global_config as gv
from main.data import global_statics as gs
from main.view import avalogue
from main.view import dialogue
from main.view import avatar_view
from main.control import jackal_ai_controller
from main.control import userAI
from main.control import event_registrar
from main.control import event_manager
from main.utils import logger
import random
import time
import threading
import pygame
import socket
import socketserver

NODE_INITIALIZED = False
csv_dialogue_s = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/s.csv"
csv_dialogue_ns = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/ns.csv"

csv_idle = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/IdleAvatars.csv"
csv_talking = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/TalkingAvatars.csv"
csv_reactive = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/spreadsheets/ReactiveAvatars.csv"

def init():
    # print("*** ARYA DEBUG LOG :: view started")
    # print(sys.argv)
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
            gv.tutorial_mode = True
            
        else:
            gv.tutorial_mode = False
            # event_manager.EventManager.post_event("freeze") # type: ignore
            sys.exit(1)
        
        if arg2 == "s":
            gv.social_mode = True
        elif arg2 == "ns":
             gv.social_mode = False
        elif arg2 == "nn":
            gv.social_mode = None
            gv.practice_mode = False
        else:
            print("Incorrect command or typo")
            sys.exit(1)
        

        
        if arg3 == '1':
            gv.practice_mode = True
            # event_manager.EventManager.post_event("freeze") # type: ignore
        elif arg3 == '0':
            gv.practice_mode = False
            # event_manager.EventManager.post_event("unfreeze") # type: ignore
        else:
            print("Incorrect command or typo")
            sys.exit(1)

    if len(sys.argv) == 3:
    
        arg1 = sys.argv[1]
        arg2 = sys.argv[2]

        gv.practice_mode = False
        gv.tutorial_mode = False
         
        gv.participant = arg1
        # print(f"*** ARYA DEBUG LOG :: PARTICIPANT ID: \"{arg1}\"")
        # print("*** ARYA DEBUG LOG: ", gv.participant)
       
        if arg2 == "s":
            gv.social_mode = True
        elif arg2 == "ns":
            gv.social_mode = False
        else:
            print("Incorrect command or typo")
            sys.exit(1)

def main(): 
    
    global NODE_INITIALIZED
    print('[Arya] View Node Activated!')

    root = tk.Tk()
    root.configure(bg=gs.DARK_BG)
    # root.geometry("1440x900")
    width, height = root.winfo_screenwidth(), root.winfo_screenheight()
    gs.load_all_pixel_info(width, height)
    
    # width, height = 1440, 900
    root.geometry('%dx%d+0+0' % (width, height))
    root.title("Jackal Teleoperator GUI")
    tabControl = ttk.Notebook(root)
    style = ttk.Style()
    style.theme_use('default')
    style.configure("TNotebook", background=gs.DARK_BG, borderwidth=0)
    style.configure("TNotebook.Tab", background=gs.BOX_HIGHLIGHT, foreground=gs.FG_COLOR)
    style.map("TNotebook.Tab", background=[("selected", gs.HOVER)], foreground=[("selected", gs.COLOR_CODE['white'])])
    tab1 = tk.Frame(tabControl)
    tab2 = tk.Frame(tabControl)
    tab1.configure(bg=gs.DARK_BG)
    tab2.configure(bg=gs.DARK_BG)
    tabControl.add(tab1, text = "Main")
    tabControl.add(tab2, text = "Inspection")
    tabControl.place(x = 5, y = 5, width=width ,height=height)
    # TODO: uncomment, commented for debugging.
    
    
    if camera.camera_available() and rg.HAS_ROS: 
        rospy.init_node("viewer", anonymous= True)
        NODE_INITIALIZED = True
        rospy.loginfo("viewer node started ...")
        axis = ac_msg.Axis()
        axis.pan = -180
        pub_axis = rospy.Publisher('/axis/cmd', ac_msg.Axis, queue_size=10)
        pub_axis.publish(axis)
        x = rospy.wait_for_message("/axis/state", ac_msg.Axis).pan
        print("Initial angle: " + str(x))

    global cs, dialogue_end
    cs = 0
    dialogue_end = 0

    widgets = widget_init(root, tab1, tab2)

    event_registrar.EventRegistrar.register_events(root, widgets)

    if not gv.tutorial_mode:
        widgets['avalogue'].set_avalogue("t_default", "start_experiment")
    else:
        widgets['avalogue'].set_avalogue("t_default", "intro_1")
    
    # fake collision detector, woz style
    # controls vision stuff, like reaching the sensor 
    # or detecting collisions via the signals sent from experimenter
    x = threading.Thread(target=server_program, args=(widgets["avalogue"],))
    x.start()
    
    def freeze(dummy = 0):
        pub.publish(True)
    
    def unfreeze(dummy = 0):
        if not NODE_INITIALIZED:
            print("No node yet, skipping publish.")
            return
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

    if rg.HAS_ROS:
        pub = rospy.Publisher("freeze", std_msg.Bool, queue_size=10)

    if gv.tutorial_mode and not gv.practice_mode:
        unfreeze()
    
    
    def tab_checker():
        # what happens if neither of the values? why cant I just put ==1 in the equation
        if tabControl.index("current") == 1:
            gv.in_inspection = True
        elif tabControl.index("current") == 0:
            gv.in_inspection = False
        
        # what is this? TODO
        tk.Tk.after(root, 100, tab_checker)
    
    tab_checker()
    

    if gv.tutorial_mode: 
        bind_keyboard(root)

    
    # TODO
    if camera.camera_available() and rg.HAS_ROS:
        print('[Arya] Camera Available.')
        try:
            tab1.mainloop()
        except rospy.ROSInterruptException:
            pass
    else:     
        print('[Arya] Camera Unavailable.')
        tab1.mainloop()

def camera_widget(root, tab1, tab2):
    pass
#############################################################################

#############################################################################
def widget_init(root, tab1, tab2):

    print('[Arya] Initializing Widgets ...')
    widgets = {}

    def initialize_camera_views():
        # widgets['view_back'] = camera.CameraView(tab1, gs.flir_info, camera.camera_available(), "flir")
        widgets['camera_front'] = camera.CameraView(tab1, gs.front_camera_info, camera.camera_available(), "flir")

    def initialize_buttons():
        pass
        # widgets['calibrate_button'] = button.BaseButton(root, gs.button_calibrate_info, activate=True, enable=False)

    def initialize_canvases():
        # widgets['countdown'] = flashing_image.CountdownCanvas(root, gs.countdown_info)
        widgets['timer_canvas'] = canvas.TimerCanvas(root, gs.timer_canvas_info)

    def initialize_labels():
        # widgets['small_label'] = labels.CameraLabel(tab1, gs.small_camera_label)
        widgets['big_label'] = labels.CameraLabel(tab1, gs.big_camera_label)
        widgets['calibrate_label'] = labels.CalibrateLabel(root, gs.clbr_label, "")
        # TODO idk what to do with this
        # widgets['calibrate_button'].add_event(widgets['calibrate_label'].activate)

        timer_label = tk.Label(root, text=gs.timer_label_info["text"], font=gs.timer_label_info["font"], fg=gs.timer_label_info["text_color"], bg=gs.DARK_BG)
        timer_label.place(x = gs.timer_label_info["x"], y = gs.timer_label_info["y"], width=gs.timer_label_info["width"], height=gs.timer_label_info["height"])
        
    def initialize_dialogue_system():
        if not gv.tutorial_mode or gv.practice_mode:
            widgets['dialogue_view'] = dialogue.DialogueView(root, gs.dialogueview_info, widgets)
            widgets['dialogue_model'] = dialogue.DialogueModel(root, csv_dialogue_ns if not gv.social_mode else csv_dialogue_s)
            widgets['avatar_view'] = avatar_view.AvatarView(root, gs.javatar_info, gv.social_mode)
            widgets['avatar_model'] = avatar_view.AvatarModel(csv_idle, csv_talking, csv_reactive)

            widgets['avalogue'] = avalogue.AvalogueController(root, widgets['dialogue_model'], widgets['dialogue_view'], widgets['avatar_model'], widgets['avatar_view'])

        else:
            widgets['avatar_view'] = None
            widgets['avatar_model'] = None
            widgets['avalogue'] = None
            widgets['dialogue_view'] = None
            widgets['dialogue_model'] = None
        widgets['dialogue_text'] = None

    def initialize_misc_components(avalogue):
        # widgets['flashing_image'] = flashing_image.FlashingImage(root, gs.flashing_image_info)
        widgets['inspection_page'] = inspection.InspectionPage(tab2, avalogue)


    # def initialize_ai():
        # widgets['jackal_ai'] = jackal_ai_controller.JackalAI(root)
        # widgets['user_ai'] = userAI.UserAI(root)

    # def initialize_finite_statemachine():   
    #     if not gv.tutorial_mode:
    #         ui_fsm = state.TeleopGUIMachine(widgets)  
    #     else:
    #         ui_fsm = state.TutorialGUIMachine(widgets)
        
        # widgets['task_canvas'].add_fsm(ui_fsm)
        # widgets['timer_canvas'].add_fsm(ui_fsm)
        # widgets['countdown'].add_fsm(ui_fsm)
        # widgets['ui_fsm'] = ui_fsm


    # Call the modularized initialization functions
    initialize_camera_views()
    initialize_buttons()
    initialize_canvases()
    initialize_labels()
    initialize_dialogue_system()
    initialize_misc_components(widgets["avalogue"])
    # initialize_ai()
    # initialize_finite_statemachine()

    return widgets
#############################################################################

#############################################################################
def bind_keyboard(tab1):
# def bind_keyboard(tab1, cursor_canvas_small, cursor_canvas_big, task_canvas, view_back, camera_front, manual_button, auto_button, circle_canvas, jackal_ai, tutorial_fsm):
    
    if not gv.practice_mode:
        tab1.bind('b', lambda e: toggle_barcontroller())
        tab1.bind('x', lambda e: pygame.mixer.find_channel().play(gv.beep_sound))
        tab1.bind('z', lambda e: pygame.mixer.find_channel().play(gv.beep_sound))
        
    elif gv.practice_mode:
        tab1.bind('9', lambda e: start_tutorial(tab1))
        tab1.bind('x', lambda e: playsound_beep_thread())
        tab1.bind('z', lambda e: playsound_beep_thread())       
    
def start_tutorial(tab):
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
    # t_fsm.initializing_to_start()

def server_program(widgets):
    socketserver.TCPServer.allow_reuse_address = True

    # collision detector device
    HOST = '192.168.2.168'
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
                    conn.settimeout(None)
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
                    
                        print("*** Arya From connected user: " + data)
                        if int(data) == 0:
                            logger.Logger.log("paper", 1) # type: ignore
                            event_manager.EventManager.post_event("paper_reach") # type: ignore
                        else:
                            logger.Logger.log("collision", data) # type: ignore
                            event_manager.EventManager.post_event("avalogue_collision") # type: ignore
            
            except Exception as e:
                print("ERROR happened: " + str(e))  
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

# def joy_config(data, widgets):
#     global rb1, rb2normal, rb3, cs, dialogue_end

#     jackal_ai = widgets["jackal_ai"]

#     if gv.in_inspection:
#         return


#     # end the dialogue talking sound and show all the text
#     dialogue_end_buff = dialogue_end
#     dialogue_end = data.buttons[5]
#     if dialogue_end == 1 and dialogue_end_buff == 0:
#         event_manager.EventManager.post_event("stop_talking", 1) # type: ignore

def playsound_beep_thread():
    x = threading.Thread(target=playsound("/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/sounds/beep.wav"))   
    x.start()

def playsound_animalese_thread():
    x = threading.Thread(target=playsound(random.choice(gv.animalese_sound_dir)))
    x.start

if __name__ == "__main__":
    init()
    main()
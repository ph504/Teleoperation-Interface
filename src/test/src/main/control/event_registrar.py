import sys
# control/event_registrar.py
from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

from main.utils import ros_guard as rg
if rg.HAS_ROS:
    import rospy
    import std_msgs.msg as std_msg

from main.model import event_model
from main.control import event_manager
from main.control import teleop_wheel
# from main.utils import logger
from tkinter import ACTIVE as tk_ACTIVE
from tkinter import DISABLED as tk_DISABLED
# import std_msgs.msg as std_msg
# import rospy

class EventRegistrar:
    # def register_all(widgets):
    #     pass
    
    @staticmethod
    def register_events(root, widgets):
        
        # rospy.init_node('event_registrar_node', anonymous=True)
        
        def on_freeze_all(widgets): 
            # for all the selected widgets, make them frozen
            for widget_name in widgets:
                widgets[widget_name].config(state=tk_DISABLED)

        def on_freeze(widget_name, widgets):
            # deactivate active widget
            widgets[widget_name].config(state=tk_DISABLED)
            
        def on_unfreeze_all(widgets):
            # for all the selected widgets, make them unfrozen
            for widget_name in widgets:
                widgets[widget_name].config(state=tk_ACTIVE)
        
        def on_unfreeze(widget_name, widgets):
            # activate frozen/deactivated widget
            widgets[widget_name].config(state=tk_ACTIVE)

        def on_freeze_controls(switch):
            # print(f"*** ARYA DEBUG LOG :: freeze var is set to {switch}")
            if switch:
                # freeze the teleop wheel
                # freeze the time
                widgets['timer_canvas'].pause()
            else:
                # print(f"*** ARYA DEBUG LOG :: freeze var is set to {switch}")
                # print(f"*** ARYA DEBUG LOG :: freeze var is set to {switch}")

                widgets['timer_canvas'].start()
            rospy.Publisher("freeze", std_msg.Bool, queue_size=10).publish(switch)
            # print(f"*** ARYA DEBUG LOG :: freeze var is set to {switch}")

        def inspection_success(widgets):
            # print(f"*** ARYA DEBUG LOG :: AVALOGUE IS THE PROBLEM THIS IS OKAY")
            widgets["avalogue"].on_success()

        def terminate():
            root.destroy()
            sys.exit(0)


        # updates the timestamp for the logger
        # time is string type
        # def logger_timestamp(time):
        #     logger.Logger.elapsed_time = time

        # def switch_controls(switch):
        #     print(f"*** ARYA DEBUG LOG :: freeze var is {teleop_wheel.freeze_var}")
        #     print(f"*** ARYA DEBUG LOG :: freeze var is set to {switch}")

        event_handlers = {
            event_model.EVENTS["FREEZE"]: [
                # for the above code we might want to pass in as an argument for dynamicity (ros_publisher)
                # what does this even accomplish
                # I changed the definition to the opposite, at it was ACTIVE before

                # I don't know if the widgets arguments passing is necessary but I will try after fixing all this, getting one clean run should be the blessing
                lambda widget_name : on_freeze(widget_name, widgets),
                lambda : rospy.Publisher("freeze", std_msg.Bool, queue_size=10).publish(True), 
                
                
            ],
            event_model.EVENTS["UNFREEZE"]: [
                lambda widget_name : on_unfreeze(widget_name, widgets) 
            ],
            event_model.EVENTS["FREEZE_ALL"]: [
                lambda : on_freeze_all(widgets)
            ],
            event_model.EVENTS["UNFREEZE_ALL"]: [
                lambda : on_unfreeze_all(widgets)
            ],
            # event_model.EVENTS["CALIBRATE"]: [
            #     lambda: ,
            # ]
            event_model.EVENTS["CALIBRATE_START"]: [
                # probably two unrelated events
                lambda : widgets['timer_canvas'].start(),
                # should probably disable using the unfreeze event
                lambda : widgets['calibrate_button'].enable(),
            ],
            event_model.EVENTS["CALIBRATE_PAUSE"]: [
                # probably two unrelated events
                lambda : widgets['timer_canvas'].stop(),
                # should probably disable using the freeze event
                lambda : widgets['calibrate_button'].disable(),
            ],
            event_model.EVENTS["JOY"]: [
                # lambda: widgets : ,
            ],
            event_model.EVENTS["DIALOGUE_WAIT_RESPONSE"]: [
                lambda : widgets["avalogue"].wait_for_button(),
            ],
            event_model.EVENTS["DIALOGUE_ANSWER"]: [
                lambda : widgets['avalogue'].btnpress_event()
            ],
            event_model.EVENTS["FREEZE_CONTROLS"]: [
                lambda switch : on_freeze_controls(switch), 
            ],
            event_model.EVENTS["PAPER_REACH"]: [
                lambda : widgets["avalogue"].paper_reach()
            ],
            event_model.EVENTS["AVALOGUE_COLLISION"]: [
                lambda : widgets["avalogue"].on_collision()
            ],
            event_model.EVENTS["AVALOGUE_MISTAKE"]: [
                lambda : widgets['avalogue'].on_mistake() 
            ],
            event_model.EVENTS["AVALOGUE_CONGRATULATIONS"]: [
                lambda : widgets['avalogue'].on_congrats()
            ],
            # event_model.EVENTS["COUNTDOWN"]: [
            #     lambda time : logger_timestamp(time)
            # ],
            # changes the wait flag to True, waits if the network connection is faulty, 
            # but this doesn't make sense, because it's talking about count in canvas that I don't know what it is for. 
            # So I am curious what happens if I just remove that. same goes for congratulations
            event_model.EVENTS["TRY_AGAIN"]: [
                lambda : widgets['inspection_page'].try_again()
            ],
            event_model.EVENTS["INSPECTION_SUCCESS"]: [
                lambda : inspection_success(widgets)
            ],
            event_model.EVENTS["CLEAR_WAIT_FLAG"]: [
                lambda : widgets['inspection_page'].clear_wait_flag()
            ],
            # event_model.EVENTS["USER_RESET"]: [
            #     lambda canvas : widgets['user_ai'].bar_hit_slow(canvas)
            # ],
            # event_model.EVENTS["YELLOW_MODE"]: [
            #     lambda canvas : widgets['jackal_ai'].press_yellow(canvas),
            #     lambda canvas : widgets['user_ai'].normal_counterback(canvas)
            # ],
            # event_model.EVENTS["RED_INIT_MODE"]: [
            #     lambda canvas : widgets['jackal_ai'].press_red_init(canvas),
            #     lambda canvas : widgets['jackal_ai'].mode_switchter(canvas)
            # ],
            # # TODO check the type arg
            # event_model.EVENTS["STEP_ERROR_DANGER"]: [
            #     lambda widgets, type : widgets['jackal_ai'].subtract_score(type),
            # ],
            # # TODO check the type arg
            # event_model.EVENTS["ASSISTED_SECOND"]: [
            #     lambda widgets, type : widgets['jackal_ai'].second_round(type),
            # ],
            # event_model.EVENTS["START_CNTDWN"]: [
            #     lambda : widgets['ui_fsm'].start_cntdwn(),
            # ],
            # event_model.EVENTS["MANUAL_SECOND"]: lambda: ,
            # TODO check the type arg
            # event_model.EVENTS["MANUAL_SECOND"]: [
            #     lambda type : widgets['jackal_ai'].second_round(type),
            #     lambda type : widgets['user_ai'].second_round(type),
            # ],
            event_model.EVENTS["COLOR_TRANS"]: [
                # lambda widgets : widgets['view_back'].color_transition(),
                lambda : widgets['camera_front'].color_transition(),
                # lambda widgets : widgets['circle_canvas'].color_transition(),
            ],
            # event_model.EVENTS["TALKING_STARTED"]: lambda: ,      # avatar raw disabled
            # event_model.EVENTS["TALKING_ENDED"]: lambda: ,        # avatar raw disabled
            # event_model.EVENTS["TALKING_STARTED_SAD"]: lambda: ,  # avatar raw disabled
            # event_model.EVENTS["STOP_TALKING"]: lambda: ,         # avatar raw disabled

            # event_model.EVENTS["MOVE_BAR_BACKWARD"]: lambda: ,    # this is for bar_canvas and it was deleted.
            # event_model.EVENTS["BAR_SLOW_MODE"]: lambda: ,        # this is for bar_canvas and it was deleted.
            # event_model.EVENTS["BAR_FAST_MODE"]: lambda: ,        # this is for bar_canvas and it was deleted.
            # event_model.EVENTS["BAR_ULTRA_MODE"]: lambda: ,       # this is for bar_canvas and it was deleted.
            
            # event_model.EVENTS["COUNT_MANUAL_TRANS_DEACTIVE"]: lambda: ,  # bar_canvas disabled.
            # event_model.EVENTS["COUNT_MANUAL_TRANS_ACTIVE"]: lambda: ,    # bar_canvas disabled.
            # event_model.EVENTS["RED_MODE"]: lambda: ,                     # bar_canvas disabled

            event_model.EVENTS["BUTTON_ACTIVATE"]: [
                # lambda widgets, tag : widgets['manual_button'].enable_event(tag),
                # lambda widgets, tag : widgets['auto_button'].enable_event(tag),
                lambda tag : widgets['calibrate_button'].enable_event(tag),
            ],
            # event_model.EVENTS["TASK_COUNT"]: lambda: ,               # score canvas was disabled.
            # event_model.EVENTS["STEP_ERROR"]: lambda: ,               # this is in the jackal ai controller code but it uses the bar canvas which was removed.
            # event_model.EVENTS["THRESHOLD_CROSS"]: lambda: ,          # score canvas and bar canvas were disabled.
            # event_model.EVENTS["THRESHOLD_CROSS_DANGER"]: lambda: ,   # score canvas and bar canvas were disabled.
            # event_model.EVENTS["COLLISION_HIT"]: lambda: ,            # score canvas was disabled.
            # event_model.EVENTS["WRONG_ENTRY"]: lambda: ,              # score canvas was disabled.
            # event_model.EVENTS["DUPLICATE_ENTRY"]: lambda: ,          # score canvas was disabled.
            # event_model.EVENTS["LABEL_CAMERA_SWITCH"]: lambda: ,
            event_model.EVENTS["LABEL_CAMERA_SWITCH"]: [
                lambda tag : widgets['small_label'].switch_camera(),
                lambda tag : widgets['big_label'].switch_camera(),
            ],
            # event_model.EVENTS["TOGGLE_BAR"]: lambda:                         # toggle bar is not apparent.
            # event_model.EVENTS["STATE_INITIALIZING"]: [ lambda widgets :],    # state disabled
            # event_model.EVENTS["STATE_START"]: lambda: ,                      # state disabled
            # event_model.EVENTS["STATE_DANGER1_START"]: lambda: ,              # state disabled                
            # event_model.EVENTS["STATE_DANGER1_END"]: lambda: ,                # state disabled  
            # event_model.EVENTS["STATE_DANGER2_START"]: lambda: ,              # state disabled
            # event_model.EVENTS["STATE_DANGER2_END"]: lambda: ,                # state disabled  
            # event_model.EVENTS["STATE_DECISION_PROMPT"]: lambda: ,            # state disabled  
            # event_model.EVENTS["STATE_DECISION_OUTCOME"]: lambda: ,           # state disabled 
            # event_model.EVENTS["STATE_DANGER3_START"]: lambda: ,              # state disabled
            # event_model.EVENTS["STATE_DANGER3_END"]: lambda: ,                # state disabled  
            # event_model.EVENTS["STATE_TERMINATION"]: lambda: ,                # state disabled
            event_model.EVENTS["EMERGENCY"]: [
                lambda : widgets['avalogue'].on_emergency()
            ],  
            event_model.EVENTS["TERMINATE"]: [
                lambda : terminate()
            ]
        }
        for event, handlers in event_handlers.items():
            event_manager.EventManager.register_event(event)
            
            # if isinstance(handlers, list): 
            # changed the definition to all lists
            for handler in handlers:
                event_manager.EventManager.subscribe(event)(handler)
            # else:
            #     @event_manager.EventManager.subscribe(event)
            #     def wrapped_handler():
            #         return handler()


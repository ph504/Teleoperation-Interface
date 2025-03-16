# control/event_registrar.py

import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src')

from main.model import event_model
from main.control import event_manager
from main.utils import logger
from tkinter import ACTIVE as tk_ACTIVE
from tkinter import DISABLED as tk_DISABLED
# import std_msgs.msg as std_msg
# import rospy

class EventRegistrar:
    # def register_all(widgets):
    #     pass
    @staticmethod
    def register_events():
        
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

        # updates the timestamp for the logger
        # time is string type
        def logger_timestamp(time):
            logger.Logger.elapsed_time = time

        event_handlers = {
            event_model.EVENTS["FREEZE"]: [
                # lambda : rospy.Publisher("freeze", std_msg.Bool, queue_size=10).publish(True), 
                # for the above code we might want to pass in as an argument for dynamicity (ros_publisher)
                # what does this even accomplish
                # I changed the definition to the opposite, at it was ACTIVE before

                # I don't know if the widgets arguments passing is necessary but I will try after fixing all this, getting one clean run should be the blessing
                lambda widget_name, widgets : on_freeze(widget_name, widgets)
            ],
            event_model.EVENTS["UNFREEZE"]: [
                lambda widget_name, widgets : on_unfreeze(widget_name, widgets) 
            ],
            event_model.EVENTS["FREEZE_ALL"]: [
                lambda widgets : on_freeze_all(widgets)
            ],
            event_model.EVENTS["UNFREEZE_ALL"]: [
                lambda widgets : on_unfreeze_all(widgets)
            ],
            # event_model.EVENTS["CALIBRATE"]: [
            #     lambda: ,
            # ]
            event_model.EVENTS["CALIBRATE_START"]: [
                # probably two unrelated events
                lambda widgets : widgets['timer_canvas'].start(),
                # should probably disable using the unfreeze event
                lambda widgets : widgets['calibrate_button'].enable(),
            ],
            event_model.EVENTS["CALIBRATE_PAUSE"]: [
                # probably two unrelated events
                lambda widgets : widgets['timer_canvas'].stop(),
                # should probably disable using the freeze event
                lambda widgets : widgets['calibrate_button'].disable(),
            ],
            event_model.EVENTS["JOY"]: [
                # lambda: widgets : ,
            ],            
            event_model.EVENTS["AVALOGUE_COLLISION"]: [
                lambda widgets : widgets['avalogue'].on_collision()
            ],
            event_model.EVENTS["AVALOGUE_MISTAKE"]: [
                lambda widgets : widgets['avalogue'].on_mistake() 
            ],
            event_model.EVENTS["AVALOGUE_CONGRATULATIONS"]: [
                lambda widgets : widgets['avalogue'].on_congrats()
            ],
            event_model.EVENTS["COUNTDOWN"]: [
                lambda time : logger_timestamp(time)
            ],
            # changes the wait flag to True, waits if the network connection is faulty, 
            # but this doesn't make sense, because it's talking about count in canvas that I don't know what it is for. 
            # So I am curious what happens if I just remove that. same goes for congratulations
            event_model.EVENTS["TRY_AGAIN"]: [
                lambda widgets : widgets['inspection_page'].try_again()
            ],
            event_model.EVENTS["CLEAR_WAIT_FLAG"]: [
                lambda widgets : widgets['inspection_page'].clear_wait_flag()
            ],
            event_model.EVENTS["USER_RESET"]: [
                lambda widgets, canvas : widgets['user_ai'].bar_hit_slow(canvas)
            ],
            event_model.EVENTS["YELLOW_MODE"]: [
                lambda widgets, canvas : widgets['jackal_ai'].press_yellow(canvas),
                lambda widgets, canvas : widgets['user_ai'].normal_counterback(canvas)
            ],
            event_model.EVENTS["RED_INIT_MODE"]: [
                lambda widgets, canvas : widgets['jackal_ai'].press_red_init(canvas),
                lambda widgets, canvas : widgets['jackal_ai'].mode_switchter(canvas)
            ],
            event_model.EVENTS["STEP_ERROR_DANGER"]: [
                lambda widgets, type : widgets['jackal_ai'].subtract_score(type),
            ],
            event_model.EVENTS["ASSISTED_SECOND"]: [
                lambda widgets, type : widgets['jackal_ai'].second_round(type),
            ],
            event_model.EVENTS["START_CNTDWN"]: [
                lambda gui, type : widgets['gui'].start_cntdwn(),
            ],
            # event_model.EVENTS["STATE_INITIALIZING"]: [
            #     lambda widgets : 
            # ],
            # event_model.EVENTS["STATE_START"]: lambda: ,
            # event_model.EVENTS["STATE_DANGER1_START"]: lambda: ,
            # event_model.EVENTS["STATE_DANGER1_END"]: lambda: ,
            # event_model.EVENTS["STATE_DANGER2_START"]: lambda: ,
            # event_model.EVENTS["STATE_DANGER2_END"]: lambda: ,
            # event_model.EVENTS["STATE_DECISION_PROMPT"]: lambda: ,
            # event_model.EVENTS["STATE_DECISION_OUTCOME"]: lambda: ,
            # event_model.EVENTS["STATE_DANGER3_START"]: lambda: ,
            # event_model.EVENTS["STATE_DANGER3_END"]: lambda: ,
            # event_model.EVENTS["STATE_TERMINATION"]: lambda: ,
            # event_model.EVENTS["MANUAL_SECOND"]: lambda: ,
            # event_model.EVENTS["MOVE_BAR_BACKWARD"]: lambda: ,
            # event_model.EVENTS["BAR_SLOW_MODE"]: lambda: ,
            # event_model.EVENTS["BAR_FAST_MODE"]: lambda: ,
            # event_model.EVENTS["BAR_ULTRA_MODE"]: lambda: ,
            # event_model.EVENTS["COLOR_TRANS"]: lambda: ,
            # event_model.EVENTS["TALKING_STARTED"]: lambda: ,
            # event_model.EVENTS["TALKING_ENDED"]: lambda: ,
            # event_model.EVENTS["TALKING_STARTED_SAD"]: lambda: ,
            # event_model.EVENTS["STOP_TALKING"]: lambda: ,
            # event_model.EVENTS["COUNT_MANUAL_TRANS_DEACTIVE"]: lambda: ,
            # event_model.EVENTS["COUNT_MANUAL_TRANS_ACTIVE"]: lambda: ,
            # event_model.EVENTS["RED_MODE"]: lambda: ,
            # event_model.EVENTS["BUTTON_ACTIVATE"]: lambda: ,
            # event_model.EVENTS["TASK_COUNT"]: lambda: ,
            # event_model.EVENTS["STEP_ERROR"]: lambda: ,
            # event_model.EVENTS["THRESHOLD_CROSS"]: lambda: ,
            # event_model.EVENTS["THRESHOLD_CROSS_DANGER"]: lambda: ,
            # event_model.EVENTS["COLLISION_HIT"]: lambda: ,
            # event_model.EVENTS["WRONG_ENTRY"]: lambda: ,
            # event_model.EVENTS["DUPLICATE_ENTRY"]: lambda: ,
            # event_model.EVENTS["LABEL_CAMERA_SWITCH"]: lambda: ,
            # event_model.EVENTS["TOGGLE_BAR"]: lambda: 
        }
        for event, handlers in event_handlers.items():
            event_manager.EventManager.register_event(event)
            
            # if isinstance(handlers, list): 
            # changed the definition to all lists
            for handler in handlers:
                @event_manager.EventManager.subscribe(event)(handler)
            # else:
            #     @event_manager.EventManager.subscribe(event)
            #     def wrapped_handler():
            #         return handler()


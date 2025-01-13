from collections import defaultdict
from sensor_msgs.msg import CompressedImage
from event_manager import EventManager

EVENT_FREEZE = "freeze"
EVENT_UNFREEZE = "unfreeze"
EVENT_CALIBRATE = "calibrate"
EVENT_CALIBRATE_PAUSE = "calibrate_pause"
EVENT_JOY = "joy"
EVENT_COLLISION = "collision"
EVENT_CONGRATULATIONS = "congratulations"

# Register all events
EventManager.register_event(EVENT_FREEZE)
EventManager.register_event(EVENT_UNFREEZE)
EventManager.register_event(EVENT_CALIBRATE)
EventManager.register_event(EVENT_CALIBRATE_PAUSE)


# class EventManager():

#     _subscribers = defaultdict(list)

#     def subscribe(event_type, fn):
#         EventManager._subscribers[event_type].append(fn)

#     def post_event(event_type, data=None): 
        
#         if event_type in EventManager._subscribers:
#             for fn in EventManager._subscribers[event_type]:
#                 if data is None:
#                     fn(event_type)
#                 else:
#                     fn(data)

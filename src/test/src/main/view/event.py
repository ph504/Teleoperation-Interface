from collections import defaultdict
from sensor_msgs.msg import CompressedImage


class EventManager():

    _subscribers = defaultdict(list)

    def subscribe(event_type, fn):
        EventManager._subscribers[event_type].append(fn)

    def post_event(event_type, data=None): 
        
        if event_type in EventManager._subscribers:
            for fn in EventManager._subscribers[event_type]:
                if data is None:
                    fn(event_type)
                else:
                    fn(data)

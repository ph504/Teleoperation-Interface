from collections import defaultdict
from sensor_msgs.msg import CompressedImage


class EventManager():

    subscribers = defaultdict(list)
    
    
    def __init__():
        pass
        

    def subscribe(event_type, fn):
        EventManager.subscribers[event_type].append(fn)

    def post_event(event_type, data=None): 
        
        if event_type in EventManager.subscribers:
            for fn in EventManager.subscribers[event_type]:
                if data is None:
                    fn(event_type)
                else:
                    fn(data)

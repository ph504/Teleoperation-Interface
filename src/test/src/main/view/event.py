from collections import defaultdict
from sensor_msgs.msg import CompressedImage

subscribers = defaultdict(list)

print("heiii!")

def subscribe(event_type, fn):
    subscribers[event_type].append(fn)

def post_event(event_type, data=None): 
    
    if event_type in subscribers:
        for fn in subscribers[event_type]:
            if data is None:
                fn(event_type)
            else:
                fn(data)
                


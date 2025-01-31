import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/')

class EventManager:
    _subscribers = {}
    _registered_events = set()

    @staticmethod
    def register_event(event_name):
        """Register an event name in the system."""
        if event_name in EventManager._registered_events:
            raise ValueError(f"Event '{event_name}' already registered!")
        EventManager._registered_events.add(event_name)


    @staticmethod
    def subscribe(event_name):
        """Subscribe a handler only if the event is registered."""
        if event_name not in EventManager._registered_events:
            raise ValueError(f"Event '{event_name}' not registered!")
        
        def decorator(func):
            if event_name not in EventManager._subscribers:
                EventManager._subscribers[event_name] = []
            EventManager._subscribers[event_name].append(func)
            return func
        return decorator


    @staticmethod
    def post_event(event_name, *args, **kwargs):
        """Trigger event and call all subscribers."""
        if event_name in EventManager._subscribers:
            for handler in EventManager._subscribers[event_name]:
                handler(*args, **kwargs)
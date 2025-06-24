from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

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
    def subscribe(event):
        """Subscribe a handler only if the event is registered."""
        if event not in EventManager._registered_events:
            raise ValueError(f"Event '{event}' not registered!")
        
        def decorator(func):
            if event not in EventManager._subscribers:
                EventManager._subscribers[event] = []
            EventManager._subscribers[event].append(func)
            return func
        return decorator
    
    @staticmethod
    def subscribe_handler(event, handler):
        if event not in EventManager._registered_events:
            raise ValueError(f"[ERROR] Event '{event}' is not registered!")
        
        if event not in EventManager._subscribers:
                EventManager._subscribers[event] = []

        EventManager._subscribers[event].append(handler)
        print(f"[INFO] Subscribed handler to event: {event}")
        


    @staticmethod
    def post_event(event_name, *args, **kwargs):
        # print(f"*** ARYA DEBUG LOG :: subscribers: {EventManager._subscribers}")
        """Trigger event and call all subscribers."""
        if event_name in EventManager._subscribers:
            for handler in EventManager._subscribers[event_name]:
                handler(*args, **kwargs)

        # return EventManager._subscribers!={}
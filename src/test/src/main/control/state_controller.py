from control.state_manager import StateManager

class StateController:
    def __init__(self):
        self.state_manager = StateManager()
        self.event_manager = EventManager()

    def start(self):
        self.state_manager.initializing_to_start()

    def handle_event(self, event):
        if event == "start":
            self.state_manager.initializing_to_start()
        elif event == "danger":
            self.state_manager.start_to_danger1_start()
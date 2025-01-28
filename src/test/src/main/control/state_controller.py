import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/model/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/control/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/view/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/utils/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/test/')
sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/data/')

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
            self.state_manager.start_to_danger1_start()z
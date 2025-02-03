import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/')

import sys
from tkinter import Tk
from main.control import event_manager
from main.control import event_registrar
from main.view import view  # Import your UI

def main():
    # Initialize Event System
    EventRegistrar.register_events()

    # Initialize GUI
    root = Tk()
    app = MainView(root)  # Create the view
    root.mainloop()

if __name__ == "__main__":
    main()

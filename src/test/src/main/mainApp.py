from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

from tkinter import Tk
from main.control import event_manager
from main.control import event_registrar
from main.view import view  # Import your UI

def main():
    # Initialize Event System
    event_registrar.EventRegistrar.register_events()

    # Initialize GUI
    root = Tk()
    app = MainView(root)  # Create the view
    root.mainloop()

if __name__ == "__main__":
    main()

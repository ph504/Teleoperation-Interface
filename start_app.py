import sys
import os

def replace_file_content(full_path, NEW_PATH, OLD_PATH):
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # print(f"looking for the old path {OLD_PATH} in {full_path}")
        if OLD_PATH in content:
            new_content = content.replace(OLD_PATH, NEW_PATH)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            # print(f"✅ Replaced in {full_path}")

        # else:
        #     print(f"No changes in {full_path}")
            
    except Exception as e:
        print(f"⚠️ Skipped {full_path}: {e}")


# ✅ Path replacement, the path from previous machine to this one
def replace_hardcoded_paths():
    print("[Launcher] Replacing hardcoded paths (slash-agnostic)...")

    OLD_PATH = "C:/APH508/UNB/Thesis/Teleoepration-Interface/Teleoperation-Interface"
    NEW_PATH = os.getcwd()
    NEW_PATH = NEW_PATH.replace("\\", "/")

    for dirpath, _, filenames in os.walk("."):
        for file in filenames:
            # Only process text file types
            if not file.endswith((".sh", ".py", ".txt", ".csv", ".json")):
                continue
            
            full_path = os.path.join(dirpath, file)
            # if file.endswith((".py", ".json", ".sh")):
            #     replace_file_content(full_path, NEW_PYPATH, OLD_PATH)
            
            # else:
            replace_file_content(full_path, NEW_PATH, OLD_PATH)
            

replace_hardcoded_paths()

# Hardcode the real project path where "main" lives
ABSOLUTE_PROJECT_PATH = "C:/APH508/UNB/Thesis/Teleoepration-Interface/Teleoperation-Interface/src/test/src"
ABSOLUTE_PROJECT_ROOT = "C:/APH508/UNB/Thesis/Teleoepration-Interface/Teleoperation-Interface/"
PYTHON_EXECUTABLE = sys.executable

if ABSOLUTE_PROJECT_PATH not in sys.path:
    sys.path.insert(0, ABSOLUTE_PROJECT_PATH)
import subprocess
import time
import platform
import tkinter as tk
from tkinter import messagebox

# # 👇 Ensure Python sees the project root to resolve `main.*` modules
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# if project_root not in sys.path:
#     sys.path.insert(0, project_root)

from main.utils import ros_guard as rg
from main.data import global_statics as gs


# ✅ ROS optional imports
if rg.HAS_ROS:
    import rospy
    import geometry_msgs.msg as geo_msg
    import sensor_msgs.msg as sen_msg
    import axis_camera.msg as ac_msg
    import std_msgs.msg as std_msg

TELEOP_CAMERA_MODULE = "src/test/src/main/control/teleop_camera.py"
TELEOP_WHEEL_MODULE = "src/test/src/main/control/teleop_wheel.py"
VIEW_MODULE = "src/test/src/main/view/view.py"
            
def launch_camera():
    if platform.system() == "Windows":
        # os.system(f'start python {VIEW_MODULE} {" ".join(args)}')
        os.system(f'start {PYTHON_EXECUTABLE} {ABSOLUTE_PROJECT_ROOT}{TELEOP_CAMERA_MODULE}')
    else:
        os.system(f'{PYTHON_EXECUTABLE} {ABSOLUTE_PROJECT_ROOT}{TELEOP_CAMERA_MODULE} &')
    time.sleep(5)

def launch_wheel():
    if platform.system() == "Windows":
        # os.system(f'start python {VIEW_MODULE} {" ".join(args)}')
        os.system(f'start {PYTHON_EXECUTABLE} {ABSOLUTE_PROJECT_ROOT}{TELEOP_WHEEL_MODULE}')
    else:
        os.system(f'{PYTHON_EXECUTABLE} {ABSOLUTE_PROJECT_ROOT}{TELEOP_WHEEL_MODULE} &')
    time.sleep(1)

def launch_view(args):
    # print(f'python {VIEW_MODULE} {" ".join(args)}')
    if platform.system() == "Windows":
        # os.system(f'start python {VIEW_MODULE} {" ".join(args)}')
        os.system(f'start {PYTHON_EXECUTABLE} {ABSOLUTE_PROJECT_ROOT}{VIEW_MODULE} {" ".join(args)}')

    else:
        os.system(f'{PYTHON_EXECUTABLE} {ABSOLUTE_PROJECT_ROOT}{VIEW_MODULE} {" ".join(args)} &')

    


def start_app(args):
    print(f"[Launcher] ROS Available: {rg.HAS_ROS}")
    replace_hardcoded_paths()
    launch_camera()
    launch_wheel()
    launch_view(args)

def open_menu():
    root = tk.Tk()
    root.title("Teleop GUI Launcher")
    root.geometry("500x500")
    root.resizable(False, False)
    
    root.configure(bg=gs.DARK_BG)

    tutorial_var = tk.BooleanVar()
    practice_var = tk.BooleanVar()
    social_var = tk.StringVar(value="s")


    # Title
    tk.Label(root, text="Welcome to HCI LAB!", font=("Helvetica", 14, "bold"),
             bg=gs.DARK_BG, fg=gs.ACCENT).pack(pady=10)

    # Checkbuttons
    tk.Checkbutton(root, text="Tutorial Mode", variable=tutorial_var,
                   bg=gs.DARK_BG, fg=gs.FG_COLOR, activebackground=gs.BOX_HIGHLIGHT,
                   activeforeground=gs.ACCENT, selectcolor=gs.BOX_HIGHLIGHT).pack(pady=2)

    tk.Checkbutton(root, text="Practice Mode (if tutorial)", variable=practice_var,
                   bg=gs.DARK_BG, fg=gs.FG_COLOR, activebackground=gs.BOX_HIGHLIGHT,
                   activeforeground=gs.ACCENT, selectcolor=gs.BOX_HIGHLIGHT).pack(pady=2)

    # Radio buttons
    tk.Label(root, text="Choose Mode:", bg=gs.DARK_BG, fg=gs.ACCENT).pack(pady=8)

    tk.Radiobutton(root, text="Social", variable=social_var, value="s",
                   bg=gs.DARK_BG, fg=gs.FG_COLOR, activebackground=gs.BOX_HIGHLIGHT,
                   activeforeground=gs.ACCENT, selectcolor=gs.BOX_HIGHLIGHT).pack()

    tk.Radiobutton(root, text="Non-Social", variable=social_var, value="ns",
                   bg=gs.DARK_BG, fg=gs.FG_COLOR, activebackground=gs.BOX_HIGHLIGHT,
                   activeforeground=gs.ACCENT, selectcolor=gs.BOX_HIGHLIGHT).pack()

    # Launch button
    tk.Button(root, text="Start", command=lambda: on_start(),
              font=("Helvetica", 12, "bold"),
              bg=gs.ACCENT, fg=gs.DARK_BG,
              activebackground=gs.HOVER, activeforeground=gs.FG_COLOR,
              relief=tk.RAISED, bd=2).pack(pady=20)
    
    # Participant ID
    tk.Label(root, text="Enter Participant ID:", bg=gs.DARK_BG, fg=gs.ACCENT).pack(pady=8)
    participant_id_var = tk.StringVar()
    tk.Entry(root, textvariable=participant_id_var, font=("Helvetica", 12), bg=gs.BOX_HIGHLIGHT,
             fg=gs.FG_COLOR, insertbackground=gs.FG_COLOR).pack(pady=4)
    

    # Participant ID
    tk.Label(root, text="Enter Participant Name:", bg=gs.DARK_BG, fg=gs.ACCENT).pack(pady=8)
    participant_name_var = tk.StringVar()
    tk.Entry(root, textvariable=participant_name_var, font=("Helvetica", 12), bg=gs.BOX_HIGHLIGHT,
             fg=gs.FG_COLOR, insertbackground=gs.FG_COLOR).pack(pady=4)
    

    # Callback to launch
    def on_start():
        tutorial = tutorial_var.get()
        practice = practice_var.get()
        social = social_var.get()
        pid = participant_id_var.get()
        pid = pid if not pid=="" else "arya_testing"
        print(f"*** ARYA DEBUG LOG :: PARTICIPANT ID: \"{pid}\"")

        if tutorial:
            args = ["tutorial", social, "0" if practice else "1"]
        else:
            args = [pid, social]

        root.destroy()
        start_app(args)

    root.mainloop()

if __name__ == "__main__":
    open_menu()

from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

import sys
import os
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


# ✅ ROS optional imports
if rg.HAS_ROS:
    import rospy
    import geometry_msgs.msg as geo_msg
    import sensor_msgs.msg as sen_msg
    import axis_camera.msg as ac_msg
    import std_msgs.msg as std_msg

TELEOP_CAMERA_MODULE = "src/test/src/main/control/teleop_camera.py"
TELEOP_WHEEL_MODULE = "main.control.teleop_wheel"
VIEW_MODULE = "main.view.view"

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
            
            
def replace_file_content(full_path, NEW_PATH, OLD_PATH):
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # print(f"looking for the old path {OLD_PATH} in {full_path}")
        if OLD_PATH in content:
            new_content = content.replace(OLD_PATH, NEW_PATH)

            with open(full_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Replaced in {full_path}")

        else:
            print(f"No changes in {full_path}")
            
    except Exception as e:
        print(f"⚠️ Skipped {full_path}: {e}")


def launch_camera():
    subprocess.exec(open(TELEOP_CAMERA_MODULE).read())
    # subprocess.Popen(
    #     [sys.executable, "-m", TELEOP_CAMERA_MODULE],
    #     cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    # )
    time.sleep(5)

def launch_wheel():
    subprocess.Popen([sys.executable, "-m", TELEOP_WHEEL_MODULE])
    time.sleep(1)

def launch_view(args):
    subprocess.call([sys.executable, "-m", VIEW_MODULE] + args)


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

    # 🎨 Custom Dark + Violet-Blue Theme
    DARK_BG = "#1e1e2f"
    FG_COLOR = "#f5f5f5"
    ACCENT = "#8c9eff"
    HOVER = "#5c6bc0"
    BOX_HIGHLIGHT = "#2c2f4a"

    
    root.configure(bg=DARK_BG)

    tutorial_var = tk.BooleanVar()
    practice_var = tk.BooleanVar()
    social_var = tk.StringVar(value="s")

    # Title
    tk.Label(root, text="Welcome to HCI LAB!", font=("Helvetica", 14, "bold"),
             bg=DARK_BG, fg=ACCENT).pack(pady=10)

    # Checkbuttons
    tk.Checkbutton(root, text="Tutorial Mode", variable=tutorial_var,
                   bg=DARK_BG, fg=FG_COLOR, activebackground=BOX_HIGHLIGHT,
                   activeforeground=ACCENT, selectcolor=BOX_HIGHLIGHT).pack(pady=2)

    tk.Checkbutton(root, text="Practice Mode (if tutorial)", variable=practice_var,
                   bg=DARK_BG, fg=FG_COLOR, activebackground=BOX_HIGHLIGHT,
                   activeforeground=ACCENT, selectcolor=BOX_HIGHLIGHT).pack(pady=2)

    # Radio buttons
    tk.Label(root, text="Choose Mode:", bg=DARK_BG, fg=ACCENT).pack(pady=8)

    tk.Radiobutton(root, text="Social", variable=social_var, value="s",
                   bg=DARK_BG, fg=FG_COLOR, activebackground=BOX_HIGHLIGHT,
                   activeforeground=ACCENT, selectcolor=BOX_HIGHLIGHT).pack()

    tk.Radiobutton(root, text="Non-Social", variable=social_var, value="ns",
                   bg=DARK_BG, fg=FG_COLOR, activebackground=BOX_HIGHLIGHT,
                   activeforeground=ACCENT, selectcolor=BOX_HIGHLIGHT).pack()

    # Launch button
    tk.Button(root, text="Start", command=lambda: on_start(),
              font=("Helvetica", 12, "bold"),
              bg=ACCENT, fg=DARK_BG,
              activebackground=HOVER, activeforeground=FG_COLOR,
              relief=tk.RAISED, bd=2).pack(pady=20)

    # Callback to launch
    def on_start():
        tutorial = tutorial_var.get()
        practice = practice_var.get()
        social = social_var.get()

        if tutorial:
            args = ["tutorial", social, "1" if practice else "0"]
        else:
            args = ["p0", social]

        root.destroy()
        start_app(args)

    root.mainloop()

if __name__ == "__main__":
    open_menu()

from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

import sys
import os
import subprocess
import time
import platform
import tkinter as tk
from tkinter import messagebox

# 🎯 Step 1: Change working directory if needed
expected_dir = os.path.join("src", "test", "src")
if not os.getcwd().endswith(expected_dir):
    print(f"[Launcher] Changing working directory to: {expected_dir}")
    os.chdir(expected_dir)

sys.path.insert(0, os.getcwd())

from main.utils import ros_guard as rg

# ✅ ROS optional imports
if rg.HAS_ROS:
    import rospy
    import geometry_msgs.msg as geo_msg
    import sensor_msgs.msg as sen_msg
    import axis_camera.msg as ac_msg
    import std_msgs.msg as std_msg

TELEOP_CAMERA_PATH = os.path.join("main", "control", "teleop_camera.py")
TELEOP_WHEEL_PATH = os.path.join("main", "control", "teleop_wheel.py")
VIEW_PATH = os.path.join("main", "view", "view.py")

# --------- ✅ Hardcoded Linux path in codebase to be replaced ---------
OLD_PATH = "/home/ph504/Desktop/Projects/Teleoperation-Interface"
NEW_PATH = os.getcwd()

def replace_hardcoded_paths():
    print("[Launcher] Checking for hardcoded paths...")

    # Walk through all directories and files starting from the current directory
    for dirpath, _, filenames in os.walk("."):
        
        # Loop through each file in the current directory
        for file in filenames:

            # Only target files with these extensions (likely to contain text-based paths)
            if not file.endswith((".py", ".txt", ".csv", ".json")):
                continue  # skip binary or unrelated files (e.g., .png, .exe)

            # Create the full path to the file
            full_path = os.path.join(dirpath, file)

            try:
                # Open the file in read mode and load its content
                with open(full_path, "r", encoding="utf-8") as f:
                    content = f.read()

                # Check if the OLD_PATH is present in the file content
                if OLD_PATH in content:
                    # Replace all occurrences of OLD_PATH with the NEW_PATH
                    content = content.replace(OLD_PATH, NEW_PATH)

                    # Write the updated content back to the same file
                    with open(full_path, "w", encoding="utf-8") as f:
                        f.write(content)

                    # Let the user know this file was updated
                    print(f"✅ Replaced in {full_path}")

            except Exception as e:
                # If there's any error (like permission issues), log it and move on
                print(f"⚠️ Skipped {full_path}: {e}")

def launch_camera():
    subprocess.Popen([sys.executable, TELEOP_CAMERA_PATH])
    time.sleep(5)


def launch_wheel():
    subprocess.Popen([sys.executable, TELEOP_WHEEL_PATH])
    time.sleep(1)


def launch_view(args):
    subprocess.call([sys.executable, VIEW_PATH] + args)


def start_app(args):
    print(f"[Launcher] ROS Available: {rg.HAS_ROS}")
    launch_camera()
    launch_wheel()
    launch_view(args)

def open_menu():
    root = tk.Tk()
    root.title("Teleop GUI Launcher")
    root.geometry("350x250")
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
    tk.Label(root, text="Welcome to Teleop GUI", font=("Helvetica", 14, "bold"),
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
    tk.Button(root, text="Start GUI", command=lambda: on_start(),
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

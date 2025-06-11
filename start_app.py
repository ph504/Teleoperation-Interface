import sys
import os
import pathlib
import re

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

    OLD_PATH = "/home/ph504/Desktop/Projects/Teleoperation-Interface"
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
ABSOLUTE_PROJECT_PATH = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src"
ABSOLUTE_PROJECT_ROOT = "/home/ph504/Desktop/Projects/Teleoperation-Interface/"
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




def ensure_ros_master():
    """Check if a ROS master is up; if not, launch one."""
    try:
        print("[Launcher] Checking for existing ROS master…")
        # Try listing nodes to see if master exists
        subprocess.run(
            ["rosnode", "list"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        print("[Launcher] ROS master is already running.")
    except subprocess.CalledProcessError:
        print("[Launcher] No ROS master detected; launching roscore…")
        # Fire up roscore in background
        subprocess.Popen(
            ["roscore"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)  # give it a moment to spin up





def ensure_ros_hostname():
    """
    ▸ 1.  Detect this VM’s primary IP   (first token of `hostname -I`)
    ▸ 2.  Export ROS_HOSTNAME / ROS_IP for *this* process + all children
    ▸ 3.  Persist the setting in ~/.bashrc (update if it’s already there)
    """
    ip_addr = subprocess.check_output(["hostname", "-I"], universal_newlines=True).split()[0]
    os.environ["ROS_HOSTNAME"] = ip_addr          # visible to every Popen we spawn
    os.environ["ROS_IP"]       = ip_addr          # some nodes look at ROS_IP instead

    # ── persist in ~/.bashrc ───────────────────────────────────────────────
    bashrc = pathlib.Path.home() / ".bashrc"
    line   = f"export ROS_HOSTNAME={ip_addr}\n"

    if bashrc.exists():
        txt = bashrc.read_text().splitlines(keepends=True)
        pattern = re.compile(r"^export +ROS_HOSTNAME=")
        found   = False
        for i, l in enumerate(txt):
            if pattern.match(l):
                txt[i] = line        # overwrite old value
                found = True
                break
        if not found:
            txt.append(line)         # add a new line
        bashrc.write_text("".join(txt))
    else:
        # rare: no ~/.bashrc yet
        bashrc.write_text(line)

    print(f"[Launcher] ROS_HOSTNAME/ROS_IP set to {ip_addr}")





def launch_joystick():
    """Start the ROS joy_node (if ROS is enabled)."""
    if not rg.HAS_ROS:
        print("[Launcher] ROS not available; skipping joystick.")
        return

    print("[Launcher] Launching joystick node…")
    # Try setting the device parameter (optional)
    try:
        subprocess.run(
            ["rosparam", "set", "joy_node/dev", "/dev/input/js1"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.5)  # brief pause
    except Exception:
        print("[Launcher] Warning: could not set joy_node/dev parameter.")

    # Now fire up the joy_node
    if platform.system() == "Windows":
        os.system("start rosrun joy joy_node")
    else:
        # print("*** ARYA DEBUG LOG :: running joy node")
        subprocess.Popen(
            ["rosnode", "kill", "/joy_node"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(0.5)  # brief pause
        subprocess.Popen(
            ["rosrun", "joy", "joy_node"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    time.sleep(1)

    # Set twist_mux selected input to joystick
    try:
        subprocess.run(
            ["rosparam", "set", "/twist_mux/selected", "joy_teleop/cmd_vel"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print("[Launcher] Set twist_mux selected input to joy_teleop/cmd_vel.")
    except Exception as e:
        print(f"[Launcher] Failed to set twist_mux input: {e}")


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
        # os.system(f'{PYTHON_EXECUTABLE} {ABSOLUTE_PROJECT_ROOT}{VIEW_MODULE} {" ".join(args)} &')
        subprocess.run([PYTHON_EXECUTABLE,
                    f"{ABSOLUTE_PROJECT_ROOT}{VIEW_MODULE}", *args])

    


def start_app(args):
    print(f"[Launcher] ROS Available: {rg.HAS_ROS}")
    if rg.HAS_ROS:
        ensure_ros_master()    # ← check/start master
        launch_joystick()      # ← try to start joystick
        ensure_ros_hostname()
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

    tutorial_var = tk.BooleanVar(value=True)
    practice_var = tk.BooleanVar()
    social_var = tk.StringVar(value="s")


    # Title
    tk.Label(root, text="Welcome to HCI LAB!", font=("Helvetica", 14, "bold"),
             bg=gs.DARK_BG, fg=gs.ACCENT).pack(pady=10)

    # Checkbuttons
    tk.Checkbutton(root, text="Tutorial Mode", variable=tutorial_var,
                   bg=gs.DARK_BG, fg=gs.FG_COLOR, activebackground=gs.BOX_HIGHLIGHT,
                   activeforeground=gs.ACCENT, selectcolor=gs.BOX_HIGHLIGHT, relief='flat', highlightthickness=0).pack(pady=2)

    tk.Checkbutton(root, text="Practice Mode (if tutorial)", variable=practice_var,
                   bg=gs.DARK_BG, fg=gs.FG_COLOR, activebackground=gs.BOX_HIGHLIGHT,
                   activeforeground=gs.ACCENT, selectcolor=gs.BOX_HIGHLIGHT, highlightthickness=0).pack(pady=2)

    # Radio buttons
    tk.Label(root, text="Choose Mode:", bg=gs.DARK_BG, fg=gs.ACCENT).pack(pady=8)

    tk.Radiobutton(root, text="Social", variable=social_var, value="s",
                   bg=gs.DARK_BG, fg=gs.FG_COLOR, activebackground=gs.BOX_HIGHLIGHT,
                   activeforeground=gs.ACCENT, highlightthickness=0, selectcolor=gs.BOX_HIGHLIGHT).pack()

    tk.Radiobutton(root, text="Non-Social", variable=social_var, value="ns",
                   bg=gs.DARK_BG, fg=gs.FG_COLOR, activebackground=gs.BOX_HIGHLIGHT,
                   activeforeground=gs.ACCENT, highlightthickness=0, selectcolor=gs.BOX_HIGHLIGHT).pack()

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
        # print(f"*** ARYA DEBUG LOG :: PARTICIPANT ID: \"{cpid}\"")

        if tutorial:
            args = ["t", social, "0" if practice else "1"]
        else:
            args = [pid, social]

        root.destroy()
        # print(f"*** ARYA DEBUG LOG :: args: \"{args}\"")

        start_app(args)

    root.mainloop()

if __name__ == "__main__":
    open_menu()

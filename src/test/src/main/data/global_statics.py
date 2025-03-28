import numpy as np
import tkinter as tk
original_width, original_height = 1920, 1080

COLOR_CODE = {
    "light_green": '#03fc0f',
    "yellow": '#ecfc03',
    "orange": '#faa94d',
    "red": "#f70505"
}

# front camera label text
big_camera_label_percent = {
    "x": 860 / original_width,
    "y": 130 / original_height,
    "width": 200 / original_width,
    "height": 20 / original_height,
    "text" : "Front Camera",
    "font": ('Helvetica', '13', 'bold')
}

button_calibrate_info_percent = {
    "x": 1615 / original_width,
    "y": 850 / original_height,
    "width": 150 / original_width,
    "height": 50 / original_height,
    "text": "Calibrate",
    "state": tk.ACTIVE,
    "tag": 7,    
}

clbr_label_percent = {
    "x": 5 / original_width,
    "y": 815 / original_height,
    "width": 300 / original_width,
    "height": 20 / original_height,
    "color": "red",
    "font": ('Helvetica', '20', 'bold')
}

axis_info_percent = {
    "x": 560 / original_width,
    "y": 90 / original_height,
    "width": 900 / original_width,
    "height": 850 / original_height,
    # "colors": {"light_green": '#03fc0f', "yellow": '#ecfc03', "orange": '#faa94d', "red": "#f70505"}
    "color" : "#ecfc03",
}

timer_canvas_info_percent = {
    "x": 1565 / original_width,  # 89.84%
    "y": 215 / original_height,  # 6.94%
    "width": 200 / original_width,  # 10.42%
    "height": 50 / original_height,  # 4.63%
    "color": "red",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}

timer_label_info_percent = {
    "x": 1640 / original_width,  # 93.75%
    "y": 200 / original_height,  # 5.56%
    "width": 50 / original_width,  # 2.60%
    "height": 17 / original_height,  # 1.57%
    "color": "blue",
    "text": "Timer",
    "font": ('Helvetica', '12', 'bold'),
}

button_freeze_info_percent = {
    "x": 1565 / original_width,
    "y": 900 / original_height,
    "width": 150 / original_width,
    "height": 50 / original_height,
    "text": "Freeze",
    "state": tk.ACTIVE,
    "tag": 6,
}

# jackal avatar info on the view
javatar_info_percent = {
    "x": 150 / original_width,
    "y": 100 / original_height,
    "width": 200 / original_width,
    "height": 180 / original_height,
}

dialogueview_info_percent = {
    "x": 50 / original_width,
    "y": 300 / original_height,
    "width": 450 / original_width,
    "height": 700 / original_height,
    "font": ('Calibri',10, 'bold', 'italic'),
    "bg": '#d9d7bd',
    "wraplength": 800 / original_width,
    

    "btn1_info_percent": {
        "x": 1250 / original_width,
        "y": 940 / original_height,
        "width": 100 / original_width,
        "height": 30 / original_height,
        "text": "Button 1", 
        
    },

    "btn2_info_percent": { 
        "x": 1350 / original_width,
        "y": 940 / original_height,
        "width": 100 / original_width,
        "height": 30 / original_height,
        "text": "Button 2",
        
    },

    "btn_info_percent": {   
        "x": 1300 / original_width,
        "y": 940 / original_height,
        "width": 100 / original_width,
        "height": 30 / original_height,
        "text": "Button",
    },

}

javatar_images = {
    "default" : "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/default/IDLE_01.png",
    "default-talking": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/default/IDLE_05.png",
    "default-blink": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/default/IDLE_04.png",
    "default-left": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/default/IDLE_02.png",
    "default-right": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/default/IDLE_03.png",
    "happy" : "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/happy/IDLE_17.png",
    "happy-blink": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/happy/IDLE_20.png",
    "sad" : "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/sad/IDLE_09.png",
    "sad-blink": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/sad/IDLE_12.png",
    "sad-talking": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/sad/IDLE_13.png",
    "angry": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/angry/IDLE_21.png",
    "angry-blink": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/JACKEL/angry/IDLE_24.png",
    "nonsocial": "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/images/non_social.png"

}

# -------------------------------------------------------- functions --------------------------------------------------------
#############################################################################
def load_all_pixel_info(screen_width, screen_height):
    # 📌 Declare all globals to assign them from inside this function
    global axis_info
    global big_camera_label, small_camera_label, clbr_label
    global big_canvas_info, small_canvas_info
    global timer_canvas_info, timer_label_info
    global task_canvas_info, task_label_info
    global dialogueview_info, dbox_info
    global button_yes_info, button_no_info, button_start_info
    global button_freeze_info, button_calibrate_info
    global countdown_info
    global javatar_info

    # 🎥 Camera views
    axis_info = convert_to_pixels(axis_info_percent, screen_width, screen_height)

    # 🏷️ Camera label overlays and calibration label
    big_camera_label = convert_to_pixels(big_camera_label_percent, screen_width, screen_height)
    clbr_label = convert_to_pixels(clbr_label_percent, screen_width, screen_height)

    # 📊 Canvases (bar indicators, timers, tasks)
    timer_canvas_info = convert_to_pixels(timer_canvas_info_percent, screen_width, screen_height)
    timer_label_info = convert_to_pixels(timer_label_info_percent, screen_width, screen_height)

    # 💬 Dialogue and button layout
    dialogueview_info = convert_to_pixels(dialogueview_info_percent, screen_width, screen_height)
    dialogueview_info["btn1_info"] = convert_to_pixels(dialogueview_info_percent["btn1_info_percent"], screen_width, screen_height)
    dialogueview_info["btn2_info"] = convert_to_pixels(dialogueview_info_percent["btn2_info_percent"], screen_width, screen_height)
    dialogueview_info["btn_info"] = convert_to_pixels(dialogueview_info_percent["btn_info_percent"], screen_width, screen_height)

    # 🎮 Buttons (mode selection, calibration, yes/no)
    button_freeze_info = convert_to_pixels(button_freeze_info_percent, screen_width, screen_height)
    button_calibrate_info = convert_to_pixels(button_calibrate_info_percent, screen_width, screen_height)


    # 🤖 Avatar (Javatar) position
    javatar_info = convert_to_pixels(javatar_info_percent, screen_width, screen_height)
    
    # return{
    #     "flir_info": flir_info,
    #     "axis_info": axis_info,
    #     "big_camera_label": big_camera_label,
    #     "small_camera_label": small_camera_label,
    #     "clbr_label": clbr_label,
    #     "big_canvas_info": big_canvas_info,
    #     "small_canvas_info": small_canvas_info,
    #     "timer_canvas_info": timer_canvas_info,
    #     "timer_label_info": timer_label_info,
    #     "task_canvas_info": task_canvas_info,
    #     "task_label_info": task_label_info,
    #     "miss_canvas_agent_info": miss_canvas_agent_info,
    #     "miss_label_agent_info": miss_label_agent_info,
    #     "miss_canvas_operator_info": miss_canvas_operator_info,
    #     "miss_label_operator_info": miss_label_operator_info,
    #     "score_canvas_info": score_canvas_info,
    #     "score_label_info": score_label_info,
    #     "circle_canvas_info": circle_canvas_info,
    #     "dialogueview_info": dialogueview_info,
    #     "dbox_info": dbox_info,
    #     "button_auto_info": button_auto_info,
    #     "button_manual_info": button_manual_info,
    #     "button_yes_info": button_yes_info,
    #     "button_no_info": button_no_info,
    #     "button_start_info": button_start_info,
    #     "button_freeze_info": button_freeze_info,
    #     "button_calibrate_info": button_calibrate_info,
    #     "flashing_image_info": flashing_image_info,
    #     "countdown_info": countdown_info,
    #     "task_inspect_info": task_inspect_info,
    #     "javatar_info": javatar_info
    # }
#############################################################################

#############################################################################
def convert_to_pixels(percent_info, screen_width, screen_height):
    scale_factor = min(screen_width/original_width, screen_height/original_height)
    wraplength = percent_info.get("wraplength", None)
    if wraplength is not None:
        wraplength = int(wraplength * screen_width)
    font = percent_info.get("font", None)
    if font is not None:
        fontsize = int(scale_factor*int(font[1]))
        font = (font[0], fontsize, font[2])

    pixel_info = {
        "x": int(percent_info["x"] * screen_width),
        "y": int(percent_info["y"] * screen_height),
        "width": int(percent_info["width"] * screen_width),
        "height": int(percent_info["height"] * screen_height),
        "endup_angle": percent_info.get("endup_angle", None),  # Keep as is
        "endleft_angle": percent_info.get("endleft_angle", None),
        "endright_angle": percent_info.get("endright_angle", None),
        "outline_color": percent_info.get("outline_color", None),  # Colors stay the same
        "outline_width": percent_info.get("outline_width", None),  # Leave unchanged
        "wraplength": wraplength,
        "text": percent_info.get("text", None), # Keep the text as is
        "color": percent_info.get("color", None),  # Colors stay the same
        "font": font,
        "active" : percent_info.get("active", None),  # Keep the boolean as is
        "state" : percent_info.get("state", None),  # Keep the state as is
        "tag" : percent_info.get("tag", None),  # Keep the tag as is
        "bg": percent_info.get("bg", None), # Keep the background color as is
    }
    return pixel_info
#############################################################################
# -------------------------------------------------------- functions --------------------------------------------------------

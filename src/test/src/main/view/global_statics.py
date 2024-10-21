import numpy as np
import tkinter as tk
original_width, original_height = 1920, 1080


big_camera_label_percent = {
    "x": 860 / original_width,
    "y": 130 / original_height,
    "width": 200 / original_width,
    "height": 20 / original_height,
    "font": ('Helvetica', '13', 'bold')
}

small_camera_label_percent = {
    "x": 120 / original_width,
    "y": 35 / original_height,
    "width": 200 / original_width,
    "height": 15 / original_height,
    
    "font": ('Helvetica', '10', 'bold')

}

clbr_label_percent = {
    "x": 5 / original_width,
    "y": 815 / original_height,
    "width": 300 / original_width,
    "height": 20 / original_height,
    "color": "red",
    "font": ('Helvetica', '9', 'bold')
}

flir_info_percent = {
    "x": 15 / original_width,
    "y": 50 / original_height,
    "width": 400 / original_width,
    "height": 300 / original_height,
    "colors": {"light_green": '#03fc0f', "yellow": '#ecfc03', "orange": '#faa94d', "red": "#f70505"}
}
axis_info_percent = {
    "x": 560 / original_width,
    "y": 150 / original_height,
    "width": 800 / original_width,
    "height": 600 / original_height,
    "colors": {"light_green": '#03fc0f', "yellow": '#ecfc03', "orange": '#faa94d', "red": "#f70505"}
}


big_canvas_info_percent = {
    "x": 1500 / original_width,  # 78.13%
    "y": 600 / original_height,  # 55.56%
    "width": 150 / original_width,  # 7.81%
    "height": 150 / original_height,  # 13.89%
    "endup_angle": np.deg2rad(-90),
    "endleft_angle": np.deg2rad(-240),
    "endright_angle": np.deg2rad(60),
    "outline_color": "SpringGreen3",
    "outline_width": 5,  # Leave unchanged
    "color": "green",
    "active": True
}

small_canvas_info_percent = {
    "x": 430 / original_width,  # 22.40%
    "y": 250 / original_height,  # 23.15%
    "width": 50 / original_width,  # 2.60%
    "height": 50 / original_height,  # 4.63%
    "endup_angle": np.deg2rad(-90),
    "endleft_angle": np.deg2rad(-240),
    "endright_angle": np.deg2rad(60),
    "outline_color": "SpringGreen3",
    "outline_width": 2,  # Leave unchanged
    "color": "green",
    "active": False
}

timer_canvas_info_percent = {
    "x": 1725 / original_width,  # 89.84%
    "y": 75 / original_height,  # 6.94%
    "width": 200 / original_width,  # 10.42%
    "height": 50 / original_height,  # 4.63%
    "color": "blue",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}

timer_label_info_percent = {
    "x": 1800 / original_width,  # 93.75%
    "y": 60 / original_height,  # 5.56%
    "width": 50 / original_width,  # 2.60%
    "height": 17 / original_height,  # 1.57%
    "color": "blue",
    "font": ('Helvetica', '12', 'bold'),
}

task_canvas_info_percent = {
    "x": 1675 / original_width,  # 87.24%
    "y": 75 / original_height,  # 6.94%
    "width": 100 / original_width,  # 5.21%
    "height": 50 / original_height,  # 4.63%
    "color": "green",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}

task_label_info_percent = {
    "x": 1700 / original_width,  # 88.54%
    "y": 60 / original_height,  # 5.56%
    "width": 50 / original_width,  # 2.60%
    "height": 17 / original_height,  # 1.57%
    "color": "green",
    "font": ('Helvetica', '12', 'bold'),
}

miss_canvas_agent_info_percent = {
    "x": 1400 / original_width,  # 72.92%
    "y": 75 / original_height,  # 6.94%
    "width": 100 / original_width,  # 5.21%
    "height": 50 / original_height,  # 4.63%
    "color": "red",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}

miss_label_agent_info_percent = {
    "x": 1425 / original_width,  # 74.22%
    "y": 60 / original_height,  # 5.56%
    "width": 50 / original_width,  # 2.60%
    "height": 17 / original_height,  # 1.57%
    "color": "red",
    "font": ('Helvetica', '12', 'bold'),
}

miss_canvas_operator_info_percent = {
    "x": 1500 / original_width,  # 78.13%
    "y": 75 / original_height,  # 6.94%
    "width": 100 / original_width,  # 5.21%
    "height": 50 / original_height,  # 4.63%
    "color": "red",
    "font": ('Helvetica', '24', 'bold'),
    "active": True
}

miss_label_operator_info_percent = {
    "x": 1515 / original_width,  # 78.91%
    "y": 60 / original_height,  # 5.56%
    "width": 70 / original_width,  # 3.65%
    "height": 17 / original_height,  # 1.57%
    "color": "red",
    "font": ('Helvetica', '12', 'bold'),
}

score_canvas_info_percent = {
    "x": 1450 / original_width,  # 75.52%
    "y": 75 / original_height,  # 6.94%
    "width": 150 / original_width,  # 7.81%
    "height": 50 / original_height,  # 4.63%
    "color": "blue",
    "font": ('Helvetica', '24', 'bold'),
    "active": False
}

score_label_info_percent = {
    "x": 1500 / original_width,  # 78.13%
    "y": 60 / original_height,  # 5.56%
    "width": 50 / original_width,  # 2.60%
    "height": 17 / original_height,  # 1.57%
    "color": "blue",
    "font": ('Helvetica', '12', 'bold'),
}

circle_canvas_info_percent = {
    "x": 1550 / original_width,  # 80.73%
    "y": 290 / original_height,  # 26.85%
    "width": 802 / original_width,  # 41.77%
    "height": 602 / original_height,  # 55.74%
    "colors": {"light_green": '#03fc0f', "yellow": '#ecfc03', "orange": '#faa94d', "red": "#f70505"},
    "active": True
}

dialogueview_info_percent = {
    "x": 660 / original_width,
    "y": 800 / original_height,
    "width": 800 / original_width,
    "height": 180 / original_height,
    "font": ('Calibri',12, 'bold', 'italic'),
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

dbox_info_percent = {
    "x": 660 / original_width,
    "y": 800 / original_height,
    "width": 800 / original_width,
    "height": 180 / original_height
}

button_auto_info_percent = {
    "x": 70 / original_width,
    "y": 500 / original_height,
    "width": 150 / original_width,
    "height": 50 / original_height,
    "text": "Assisted Mode",
    "state": tk.DISABLED,
    "tag": 1,

}

button_manual_info_percent = {
    "x": 70 / original_width,
    "y": 560 / original_height,
    "width": 150 / original_width,
    "height": 50 / original_height,
    "text": "Manual Mode",
    "state": tk.ACTIVE,
    "tag": 2,

}

button_yes_info_percent = {
    "x": 1250 / original_width,
    "y": 940 / original_height,
    "width": 100 / original_width,
    "height": 30 / original_height,
    "text": "Yes",
    "state": tk.ACTIVE,
    "tag": 3,

    
}

button_no_info_percent = {
    "x": 1350 / original_width,
    "y": 940 / original_height,
    "width": 100 / original_width,
    "height": 30 / original_height,
    "text": "No",
    "state": tk.ACTIVE,
    "tag": 3,

}

button_start_info_percent = {
    "x": 1300 / original_width,
    "y": 940 / original_height,
    "width": 100 / original_width,
    "height": 30 / original_height,
    "text": "Start",
    "state": tk.ACTIVE,
    "tag": 5,
 
    
}

button_freeze_info_percent = {
    "x": 70 / original_width,
    "y": 900 / original_height,
    "width": 150 / original_width,
    "height": 50 / original_height,
    "text": "Freeze",
    "state": tk.ACTIVE,
    "tag": 6,

    
}

button_calibrate_info_percent = {
    "x": 70 / original_width,
    "y": 800 / original_height,
    "width": 150 / original_width,
    "height": 50 / original_height,
    "text": "Calibrate",
    "state": tk.ACTIVE,
    "tag": 7,

    
}


# wtf is a javatar???
javatar_info_percent = {
    "x": 460 / original_width,
    "y": 800 / original_height,
    "width": 200 / original_width,
    "height": 180 / original_height,
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

def convert_to_pixels(percent_info, screen_width, screen_height):
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
        "color": percent_info.get("color", None),  # Colors stay the same
        "font": percent_info.get("font", None),
        "active": percent_info.get("active", None)  # Keep the boolean as is
    }
    return pixel_info

# -------------------------------------------------------- functions --------------------------------------------------------

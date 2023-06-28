from PIL import ImageTk
from tkinter import *
import rospy
from sensor_msgs.msg import CompressedImage
import cv2
import PIL.Image
import numpy as np
from event import *
from cv_bridge.core import CvBridge
import global_variables


#Make it false when you are not working with jackal
camera_available = True

flir_info = {
    "x": 15,
    "y": 50,
    "width": 400,
    "height": 300,
    "colors": {"light_green": '#03fc0f', "yellow": '#ecfc03', "orange": '#faa94d', "red": "#f70505"}
}
axis_info = {
    "x": 560,
    "y": 150,
    "width": 800,
    "height": 600,
    "colors": {"light_green": '#03fc0f', "yellow": '#ecfc03', "orange": '#faa94d', "red": "#f70505"}
}


class CameraView():
    scan_mode = False
    
    def __init__(self, root, dict_info,cam_available, camera="flir",  img_scale= 0.8, ):
        
        self.img_scale_factor = img_scale
        self.x = dict_info["x"]
        self.y = dict_info["y"]
        self.width = dict_info["width"]
        self.height = dict_info["height"]
        self.border_colors = dict_info["colors"]
        self.camera = camera
        self.state = "green"
        self.imagetk = None
        self.is_front = None
        self.cam_available = cam_available
        self.bridge = CvBridge()
        self.border_thick = 15
        self.frame = Frame(root, highlightbackground=self.border_colors["light_green"], highlightthickness=self.border_thick)
        self.frame.place_configure(x= self.x - self.border_thick, y = self.y - self.border_thick , width=self.width + self.border_thick * 2, height=self.height + self.border_thick * 2)
        self.imagewidget = Label(self.frame) 


        EventManager.subscribe("color_trans", self.color_transition)

        #??
        if cam_available == True:
            if self.camera == "flir":
                rospy.loginfo("using flir")
                self.flir_image = rospy.Subscriber("/camera/image_color/compressed", CompressedImage, self.update_image, queue_size=1)
                self.is_front = False
            else:
                rospy.loginfo("using axis")
                self.axis_image = rospy.Subscriber("axis/image_raw/compressed", CompressedImage, self.update_image, queue_size=1)
                self.is_front = True
        else:
            if self.camera == "flir":
                self.flir_image = self.image_placeholder("flir")
                self.is_front = False      
            else:
                self.axis_image = self.image_placeholder("axis")
                self.is_front = True
                  
    def update_pos(self,dict_info):
        self.x = dict_info["x"]
        self.y = dict_info["y"]
        self.width = dict_info["width"]
        self.height = dict_info["height"]
        self.is_front = not self.is_front
        self.frame.place_configure(x= self.x - self.border_thick, y = self.y - self.border_thick , width=self.width + self.border_thick * 2, height=self.height + self.border_thick * 2)
        self.imagewidget.place(x= 0, y= 0, width= self.width, height= self.height)
        
    def update_image(self, ros_data):

        
        ##converts the text/string data into an array, reads image data from array, and converts the color space to RGB (BGR is the reverse)
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)

        if CameraView.scan_mode and self.camera == "axis":
            EventManager.post_event("tag_detection", ros_data)

        #find the shape of array (number of elements in each dimensions) convert it to a number and multiply it by scale factor. The shape int number is the value of pixel numbers for width/height. multiplying just downscales/upscales it.
        new_width = int(image_np.shape[1] * self.img_scale_factor)
        new_height = int(image_np.shape[0] * self.img_scale_factor)
        new_dims = (new_width, new_height)

        #resize it based on the new dimensions calculated
        image_np = cv2.resize(image_np, new_dims)
        
        

        #convert numpy image (with array interface) to pillow image
        img = PIL.Image.fromarray(image_np).resize((self.width,self.height), PIL.Image.ANTIALIAS)
        

        
        #for displayin the image in the tkinter GUI
        self.imgtk = ImageTk.PhotoImage(image=img)
        self.imagewidget.config(image=self.imgtk)
        self.imagewidget.image = self.imgtk
        self.imagewidget.place(x= 0, y= 0, width= self.width, height= self.height)

    def image_placeholder(self, string):
        if string == "flir":
            img = PIL.Image.open("/home/pouya/catkin_ws/src/test/src/images/elden-ring.jpg").resize((self.width, self.height), PIL.Image.ANTIALIAS)
        else:
            img = PIL.Image.open("/home/pouya/catkin_ws/src/test/src/images/kirby.jpg").resize((self.width,self.height), PIL.Image.ANTIALIAS)

        
        self.imgtk = ImageTk.PhotoImage(image=img)
        self.imagewidget.config(image=self.imgtk)
        self.imagewidget.image = self.imgtk
        self.imagewidget.place(x= self.x, y= self.y, width= self.width, height= self.height)

    def change_angle(data, small, big, curr_angle):
    
        pan = data.pan
        diff = curr_angle - pan
        curr_angle = pan
        if diff == -1:
            small.rotate("right")
            big.rotate("right")
        elif diff == 1:
            small.rotate("left")
            big.rotate("left")   

    def color_transition(self, dummy = 0):
        
        if self.state == "green":
            self.frame.configure(highlightbackground=self.border_colors["yellow"])
            self.state = "yellow"
        
        elif self.state == "yellow":
            self.frame.configure(highlightbackground=self.border_colors["orange"])
            self.state = "orange"
        
        elif global_variables.tutorial_mode and self.state == "orange":
            self.frame.configure(highlightbackground=self.border_colors["red"])
            self.state = "red"

    def color_transition_reverse(self, dummy = 0):
        
        if self.state == "red":
            self.frame.configure(highlightbackground=self.border_colors["orange"])
            self.state = "orange"
        
        elif self.state == "orange":
            self.frame.configure(highlightbackground=self.border_colors["yellow"])
            self.state = "yellow"
        
        elif global_variables.tutorial_mode and self.state == "yellow":
            self.frame.configure(highlightbackground=self.border_colors["light_green"])
            self.state = "green"

#!/usr/bin/env python3

import rospy
import numpy as np
import cv2
from tkinter import *
from PIL import Image, ImageTk
from std_msgs.msg import String
from sensor_msgs.msg import CompressedImage




VERBOSE = False

class Control():
    def __init__(self, window):
        ############### Tkinter Window Properties and Setup ########
        self.window = window
        self.window.label = Label(self.window)
        self.window.label.pack(anchor=CENTER)
        
        self.imgtk = None
        
        self.axis_image = rospy.Subscriber("/axis/image_raw/compressed", CompressedImage, self.update_image,  queue_size=1)
    
    def update_image(self, ros_data):
        '''
        Function to update image from axis camera in the tkinter window
        '''
        np_arr = np.fromstring(ros_data.data, np.uint8)
        image_np = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(image_np)

        self.imgtk = ImageTk.PhotoImage(image=img)
        
        self.window.label.config(image = self.imgtk)
        self.window.label.image = self.imgtk
  
    
def main():

    window = Tk()
    window.geometry("700x550")
    window.title("Axis Output")
    
    controller = Control(window)
    
    rospy.init_node("axis_receiver", anonymous = True)
    rospy.loginfo("node started...")
    try:
        window.mainloop()
    except rospy.ROSInterruptException:
        pass

if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from axis_camera.msg import Axis



def start():

        axis_new = Axis()
        axis_new.pan = -180
        axis_new.autofocus = False
        axis_new.tilt = 90
        axis_new.zoom = 0 


        rospy.init_node('calibration')

        pub_axis = rospy.Publisher('/axis/cmd', Axis, queue_size=1)
        
        rate = rospy.Rate(8)

        while not rospy.is_shutdown():
            
            pub_axis.publish(axis_new)
            
            rate.sleep()
            

        # starts the node
        
        rospy.spin()

if __name__ == '__main__':   
        start()
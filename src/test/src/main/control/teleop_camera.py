#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from axis_camera.msg import Axis
    # Author: Andrew Dai
    # This ROS Node converts Joystick inputs from the joy node
    # into commands for turtlesim

    # Receives joystick messages (EventManager.subscribed to Joy topic)
    # then converts the joysick inputs into Twist commands
    # axis 1 aka left stick vertical controls linear speed
    # axis 0 aka left stick horizonal controls angular speed



def callback(data):
    global joystick_input

    joystick_input = data.axes[3]
       

def control_camera(joys_i):
    global next_pos
    
    
    next_pos -=  joys_i
    axis.pan =  int((next_pos + 180) % 360) - 180    
    print(next_pos,"    ", joys_i)
    


def start():
        
        global pub_axis
        global axis
        global joystick_input
        global next_pos
        
        
        
        axis = Axis()
        joystick_input = 0

        next_pos = 0 
        axis.pan = -180
        axis.autofocus = False
        axis.tilt = 0
        axis.zoom = 0 
        rospy.init_node('teleop_camera_node')

        pub_axis = rospy.Publisher('/axis/cmd', Axis, queue_size=1)

        # EventManager.subscribed to joystick inputs on topic "joy"
        #rospy.EventManager.subscriber("joy", Joy, callback)
        
        rate = rospy.Rate(8)


        while not rospy.is_shutdown():
            
            #control_camera(joystick_input)
            pub_axis.publish(axis)
            rate.sleep()
       

        
        

        # starts the node
        
        rospy.spin()

if __name__ == '__main__':   
        start()
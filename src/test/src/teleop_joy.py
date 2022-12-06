#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from axis_camera.msg import Axis

    # Author: Andrew Dai
    # This ROS Node converts Joystick inputs from the joy node
    # into commands for turtlesim

    # Receives joystick messages (subscribed to Joy topic)
    # then converts the joysick inputs into Twist commands
    # axis 1 aka left stick vertical controls linear speed
    # axis 0 aka left stick horizonal controls angular speed

def callback(data):
        twist = Twist()
        twist.linear.x = 2*data.axes[1]
        twist.angular.z = 2*data.axes[0]
        pub_jackal.publish(twist)
        
        global next_pos
        
        
        axis = Axis()
        next_pos +=  data.axes[3]
        axis.pan =  next_pos % 360
        axis.tilt = (data.axes[4] + 1) * 45
        pub_axis.publish(axis)
        #print(data.axes[3],"    ",next_pos,"    ",axis.pan)
        
        

    # Intializes everything
def start():
        
        global pub_jackal
        global pub_axis
        global next_pos

        next_pos = 45

        
        rospy.init_node('teleop_joy_node')
        pub_jackal = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        pub_axis = rospy.Publisher('/axis/cmd', Axis, queue_size=3)
        # subscribed to joystick inputs on topic "joy"
        rospy.Subscriber("joy", Joy, callback)

        # starts the node
        
        rospy.spin()

if __name__ == '__main__':   
        start()
#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from axis_camera.msg import Axis
import threading

    # Author: Andrew Dai
    # This ROS Node converts Joystick inputs from the joy node
    # into commands for turtlesim

    # Receives joystick messages (subscribed to Joy topic)
    # then converts the joysick inputs into Twist commands
    # axis 1 aka left stick vertical controls linear speed
    # axis 0 aka left stick horizonal controls angular speed



def callback(data):

        #update_nextpos(next_pos)
       control_wheel()
       




def control_camera(data):
    
    global next_pos
    global count

    axis = Axis()
    count += 1
    next_pos +=  data.axes[3] / 10
    axis.pan =  int((next_pos + 180) % 360) - 180    


    pub_camera(axis)
    print(int((next_pos + 180) % 360) - 180,"     ", data.axes[3], "    ",count)


def update_nextpos(next_pos):
    next_pos = rospy.wait_for_message("/axis/state", Axis)


def pub_camera(axis):
    pub_axis.publish(axis)

def control_wheel(data):
    twist = Twist()
    twist.linear.x = 2*data.axes[1]
    twist.angular.z = 2*data.axes[0]
    pub_jackal.publish(twist)
        
        
    # Intializes everything
def start():
        
        global pub_jackal
        global pub_axis
        global next_pos
        global count

        count = 0

       
        rospy.init_node('teleop_joy_node')
        pub_jackal = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        pub_axis = rospy.Publisher('/axis/cmd', Axis, queue_size=10)

        next_pos = rospy.wait_for_message("/axis/state", Axis).pan
        print(next_pos)
        # subscribed to joystick inputs on topic "joy"
        rospy.Subscriber("joy", Joy, callback)
        #rospy.Timer(rospy.Duration(1/30), pub_camera)
        
        

        # starts the node
        
        rospy.spin()

if __name__ == '__main__':   
        start()
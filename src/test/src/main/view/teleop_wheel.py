#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from axis_camera.msg import Axis
from event import *

global freeze_var
freeze_var = True


def callback(data):
    
    twist.linear.x = -2 * data.axes[1]
    twist.angular.z = 2 * data.axes[0]      

def start():
        global pub_jackal
        global twist
        
        twist =  Twist()
        
        count = 0
        
        def freeze(dummy1 = 0, dummy2 = 0):
            global freeze_var
            freeze_var = True

        def unfreeze(dummy2 = 1):
            global freeze_var
            freeze_var = False
            print("do something!")

                
        subscribe("freeze", freeze)
        subscribe("unfreeze", unfreeze)

        print("number of subscribers: " + str(len(subscribers["unfreeze"])))
        rospy.init_node('teleop_wheel_node')

        pub_jackal = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber("joy", Joy, callback)

        rate = rospy.Rate(30)

        while not rospy.is_shutdown():
            if freeze_var == True: pub_jackal.publish(twist)
            rate.sleep()

        rospy.spin()

if __name__ == '__main__':   
        start()


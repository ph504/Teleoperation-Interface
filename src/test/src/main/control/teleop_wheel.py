#!/usr/bin/env python3

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy
from axis_camera.msg import Axis


def callback(data):
    
    twist.linear.x = -2*data.axes[1]
    twist.angular.z = 2*data.axes[0]      

def start():
        global pub_jackal
        global twist

        twist =  Twist()

        rospy.init_node('teleop_wheel_node')

        pub_jackal = rospy.Publisher('/cmd_vel', Twist, queue_size=1)
        rospy.Subscriber("joy", Joy, callback)

        rate = rospy.Rate(30)

        while not rospy.is_shutdown():
            rospy.loginfo(twist)
            pub_jackal.publish(twist)
            rate.sleep()

        rospy.spin()

if __name__ == '__main__':   
        start()


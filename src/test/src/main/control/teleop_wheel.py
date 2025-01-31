#!/usr/bin/env python3
import sys

sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/')

import rospy
import geometry_msgs.msg as geo_msg
import sensor_msgs.msg as sen_msg
import axis_camera.msg as ac_msg
import std_msgs.msg as std_msg
from main.data import global_config as gv

global freeze_var

freeze_var = True 

def callback(data):
    # print('yesysytesyseyseyseyesysyesysey')
    # forward backward motion   
    twist.linear.x = -2 * data.axes[1]
    # turning motion
    twist.angular.z = 2 * data.axes[0]      

def start():
        global pub_jackal
        global twist
        
        twist =  geo_msg.Twist()
        
        

        def freeze_manager(data):
            print(data)
            
            global freeze_var

            if data.data:
                freeze_var = True
            else:
                freeze_var = False


        print('***Arya*** Wheel Node Activated!')

        rospy.init_node('teleop_wheel_node')
        pub_jackal = rospy.Publisher('/cmd_vel', geo_msg.Twist, queue_size=1)
        
        rospy.Subscriber("freeze", std_msg.Bool , callback=freeze_manager)
        rospy.Subscriber("joy", sen_msg.Joy, callback)

        rate = rospy.Rate(30)

        while not rospy.is_shutdown():
            # print(freeze_var)
            # if freeze_var == False: pub_jackal.publish(twist)
            pub_jackal.publish(twist)
            rate.sleep()
             

        rospy.spin()

if __name__ == '__main__':   
        start()


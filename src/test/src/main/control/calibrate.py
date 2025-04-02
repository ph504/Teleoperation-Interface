#!/usr/bin/env python3
from main.utils.path_setup import extend_path_to_root
extend_path_to_root()

from main.utils import ros_guard as rg

if rg.HAS_ROS:
        import rospy
        import geometry_msgs.msg as geo_msg
        import sensor_msgs.msg as sen_msg
        import axis_camera.msg as ac_msg
        import std_msgs.msg as std_msg

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
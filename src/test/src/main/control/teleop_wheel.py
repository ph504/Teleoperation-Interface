#!/usr/bin/env python3
# from main.utils.path_setup import extend_path_to_root
# extend_path_to_root()
import sys
import os
# from main.control import teleop_wheel

ABSOLUTE_PROJECT_PATH = "/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src"

if ABSOLUTE_PROJECT_PATH not in sys.path:
    sys.path.insert(0, ABSOLUTE_PROJECT_PATH)
# sys.path.append('/home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/')
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# # print("TEH FILE IS HERE", __file__)
# # print(project_root)
# sys.path.insert(0, project_root)

from main.data import global_config as gc
from main.utils import ros_guard as rg
if rg.HAS_ROS:
    import rospy
    import geometry_msgs.msg as geo_msg
    import sensor_msgs.msg as sen_msg
    import axis_camera.msg as ac_msg
    import std_msgs.msg as std_msg
    
from main.data import global_config as gv

# gc.freeze = False 

def callback(data):
    global twist
    # print('yesysytesyseyseyseyesysyesysey')
    # forward backward motion   
    twist.linear.x = data.axes[1]
    # turning motion
    twist.angular.z = data.axes[0]      

def start():
    if rg.HAS_ROS:
        global pub_jackal
        global twist
        
        twist =  geo_msg.Twist()
    
    

    # print(f"*** ARYA DEBUG LOG :: freeze being invoked {gc.freeze}")
    def freeze_manager(data):
        # print(f"*** ARYA DEBUG LOG :: freeze manager is being invoked and freeze is set to {data}")
        gc.freeze = data.data



    if rg.HAS_ROS:
        rospy.init_node('teleop_wheel_node')
        pub_jackal = rospy.Publisher('/cmd_vel', geo_msg.Twist, queue_size=1)
        
        rospy.Subscriber("freeze", std_msg.Bool , callback=freeze_manager)
        rospy.Subscriber("joy", sen_msg.Joy, callback)
        print('[Arya] Wheel Node Activated!')

        rate = rospy.Rate(30)

        # print(f"** ARYA DEBUG LOG :: freeze? {gc.freeze}")
        while not rospy.is_shutdown():
            # print(f"** ARYA DEBUG LOG :: freeze? {gc.freeze}")

            # print(gc.freeze)
            if not gc.freeze: pub_jackal.publish(twist)
            # pub_jackal.publish(twist)
            rate.sleep()
            

        rospy.spin()    

if __name__ == '__main__':   
        # global gc.freeze
        gc.freeze = True
        print(f"*** ARYA DEBUG LOG :: the process id in wheel: {os.getpid()}")
        start()


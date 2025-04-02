HAS_ROS = True

try:
    import rospy
    import geometry_msgs.msg as geo_msg
    import sensor_msgs.msg as sen_msg
    import axis_camera.msg as ac_msg
    import std_msgs.msg as std_msg
    
except ImportError:
    HAS_ROS = False

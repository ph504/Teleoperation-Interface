#!/bin/bash

echo "Bash Started"

echo "Activating Joystick in a seperate terminal"
gnome-terminal -- bash -c "rosrun joy joy_node ; exec bash"
echo "Joystick Activated"

python3 /home/pouya/catkin_ws/src/test/src/main/control/teleop_camera.py &

echo "Calibrating Camera ... "

sleep 3
timeout 0s kill $!

echo "Calibration Finished"
echo "Activating Controller"

python3 /home/pouya/catkin_ws/src/test/src/main/view/teleop_wheel.py &

echo "Controller is activated"
echo "Parsing Arguments ..."
echo $#
echo $1 
if [ $# -ne 1 ] && [ $# -ne 5 ]; then

    echo "Incorrect number of arguments provided"
    kill $!
fi

if [ $# -eq 1 ]; then
    arg=$1
    python3 /home/pouya/catkin_ws/src/test/src/main/view/view.py $arg
fi

if [ $# -eq 5 ]; then 
    
    arg1=$1
    arg2=$2
    arg3=$3
    arg4=$4
    arg5=$5
    python3 /home/pouya/catkin_ws/src/test/src/main/view/view.py $arg1 $arg2 $arg3 $arg4 $arg5
fi


echo "Arguments are Parsed"
echo "Automation successeful"

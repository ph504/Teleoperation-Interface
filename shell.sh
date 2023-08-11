#!/bin/bash

echo "Bash Started"

echo "Activating Joystick in a seperate terminal"
gnome-terminal -- bash -c "rosrun joy joy_node ; exec bash"
echo "Joystick Activated"

python3 /home/pouya/catkin_ws/src/test/src/main/control/teleop_camera.py &

echo "Calibrating Camera ... "

sleep 5
timeout 0s kill $!

echo "Calibration Finished"
echo "Activating Controller"

python3 /home/pouya/catkin_ws/src/test/src/main/view/teleop_wheel.py &

sleep 1
echo "Controller is activated"
echo "Parsing Arguments ..."
echo $#
echo $1 
if [ $# -ne 2 ] && [ $# -ne 4 ]; then

    echo "Incorrect number of arguments provided"
    kill $!
fi

if [ $# -eq 2 ]; then
    arg1=$1
    arg2=$2


    python3 /home/pouya/catkin_ws/src/test/src/main/view/view.py $arg1 $arg2 $arg3
fi

if [ $# -eq 4 ]; then 
    
    arg1=$1
    arg2=$2
    arg3=$3
    arg4=$4
    python3 /home/pouya/catkin_ws/src/test/src/main/view/view.py $arg1 $arg2 $arg3 $arg4
fi


echo "Arguments are Parsed"
echo "Automation successeful"

#!/bin/bash

# echo "Bash Started"

SEARCH_STRING="/home/ph504/Desktop/Projects/Teleoperation-Interface"

# Get the current directory (workspace)
REPLACEMENT_STRING=$(pwd)

# echo "Checking whether the current directory and the workspace directory are matching."

# Check if the search string is already equal to the replacement string
if [ "$SEARCH_STRING" != "$REPLACEMENT_STRING" ]; then
    find . -type f -exec sed -i "s|${SEARCH_STRING}|${REPLACEMENT_STRING}|g" {} +
fi

# Find and replace the string in all files within the directory and subdirectories


# echo "The current directory matches with the workspace directory."

# echo "Activating Joystick in a seperate terminal"
gnome-terminal -- bash -c "rosrun joy joy_node ; exec bash"
# echo "Joystick Activated"

python3 src/test/src/main/control/teleop_camera.py &

# echo "Calibrating Camera ... "

sleep 5
timeout 0s kill $!

# echo "Calibration Finished"
# echo "Activating Controller"


python3 src/test/src/main/view/teleop_wheel.py &

sleep 1
# echo "Controller is activated"
echo "Parsing Arguments ..."
# echo $#
# echo $1 
if [ $# -ne 3 ] && [ $# -ne 2 ]; then

    echo "Incorrect number of arguments provided"
    kill $!
fi

if [ $# -eq 3 ]; then
    arg1=$1
    arg2=$2
    arg3=$3

    python3 src/test/src/main/view/view.py $arg1 $arg2 $arg3
fi

if [ $# -eq 2 ]; then 
    
    arg1=$1
    arg2=$2
    
    python3 src/test/src/main/view/view.py $arg1 $arg2
fi


# echo "Arguments are Parsed"
# echo "Automation successeful"



python3 /home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/control/calibrate.py &
sleep 15
timeout 0s kill $!
python3 /home/ph504/Desktop/Projects/Teleoperation-Interface/src/test/src/main/control/teleop_camera.py &
sleep 5
timeout 0s kill $!
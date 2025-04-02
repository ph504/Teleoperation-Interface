

python3 C:\\APH508\\UNB\\Thesis\\Teleoepration-Interface\\Teleoperation-Interfacesrc\\test\\src\\main\\control\\calibrate.py &
sleep 15
timeout 0s kill $!
python3 C:\\APH508\\UNB\\Thesis\\Teleoepration-Interface\\Teleoperation-Interfacesrc\\test\\src\\main\\control\\teleop_camera.py &
sleep 5
timeout 0s kill $!
# amigo_ros2_pi
AMIGO ROS2 Support for Pi 

Sourcing ROS on the Pi:
```
. ~/ros2_humble/ros2-linux/setup.bash
```

Running the current camera control node, make sure to supply 5V to the Pi and 5V to the stepper HAT
```
cd workspaces/amigo_ros2_pi &&
source install/setup.bash &&
ros2 run camera_control controller_test_node
```

If, the permissions are not allowing you to control the motors through i2c (should not be the case and it would say it explicitly):
```
sudo groupadd i2c
sudo chown :i2c /dev/i2c-1
sudo chmod g+rw /dev/i2c-1
sudo usermod -aG i2c amigopi
```
GOALS: 
- Create ROS Action Server to execute the scan action.
- Create ROS Action Client to send goals to the scan action.
- Integrate feedback from ZEDx Mini IMU information. This is necessary because the steps are counted whether they are obstructed or not by the Adafruit MotorKit library.
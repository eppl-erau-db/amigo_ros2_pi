# amigo_ros2_pi
ROS2 Support for Pi 

Sourcing ROS:
```
. ~/ros2_humble/ros2-linux/setup.bash
sudo bash -c "source /opt/ros/humble/setup.bash && source /home/amigopi/workspaces/amigo_ros2_pi/install/setup.bash && ros2 run camera_control controller_test_node"
```

sudo bash -c ". /home/amigopi/ros2_humble/ros2-linux/setup.bash && source /home/amigopi/workspaces/amigo_ros2_pi/install/setup.bash && ros2 run camera_control controller_test_node"



sudo groupadd i2c
sudo chown :i2c /dev/i2c-1
sudo chmod g+rw /dev/i2c-1
sudo usermod -aG i2c amigopi
su root
# echo 'KERNEL=="i2c-[0-9]*", GROUP="i2c"' >> /etc/udev/rules.d/10-local_i2c_group.rules

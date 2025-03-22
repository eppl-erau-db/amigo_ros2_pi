import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/amigo-pi/amigo_ros2_pi/install/sensor_integration'

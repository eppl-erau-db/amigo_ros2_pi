import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/amigopi/workspaces/amigo_ros2_pi/install/camera_control'

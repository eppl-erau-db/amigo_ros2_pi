To add a ROS 2 service that, upon request, runs the `scan_controller_node.py` and reports its completion status, follow these steps:

**1. Create a Custom Service Definition (Optional):**

If you require specific inputs or outputs for your service, define a custom service. Otherwise, you can use the standard `std_srvs/srv/Trigger` service, which has a simple request and response structure.

**2. Implement the Service Server Node:**

This node will handle service requests by launching the `scan_controller_node.py` and monitoring its execution.

**a. Create the Service Server Script:**

In your package (e.g., `amigo_ros2_pi`), create a new Python script, `scan_controller_service.py`:

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger
import subprocess

class ScanControllerService(Node):
    def __init__(self):
        super().__init__('scan_controller_service')
        self.srv = self.create_service(Trigger, 'run_scan_controller', self.handle_service)

    def handle_service(self, request, response):
        try:
            self.get_logger().info("Launching scan_controller_node.py...")

            # Launch the scan_controller_node.py
            process = subprocess.Popen(
                ['ros2', 'run', 'amigo_ros2_pi', 'scan_controller_node.py'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            stdout, stderr = process.communicate()

            if process.returncode == 0:
                self.get_logger().info("scan_controller_node.py completed successfully.")
                response.success = True
                response.message = "scan_controller_node.py completed successfully."
            else:
                error_message = stderr.decode()
                self.get_logger().error(f"scan_controller_node.py failed: {error_message}")
                response.success = False
                response.message = f"scan_controller_node.py failed: {error_message}"

        except Exception as e:
            self.get_logger().error(f"Exception occurred: {str(e)}")
            response.success = False
            response.message = f"Exception occurred: {str(e)}"

        return response

def main(args=None):
    rclpy.init(args=args)
    node = ScanControllerService()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**b. Update `setup.py`:**

Ensure the new service node is executable. In your package's `setup.py`, add the entry point for `scan_controller_service`:

```python
entry_points={
    'console_scripts': [
        'scan_controller_service = amigo_ros2_pi.scan_controller_service:main',
        # other entry points
    ],
},
```

**3. Create a Launch File:**

To facilitate running the service server, create a launch file.

**a. Create the Launch File:**

In the `launch` directory of your package, create `scan_controller_service_launch.py`:

```python
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='amigo_ros2_pi',
            executable='scan_controller_service',
            name='scan_controller_service',
            output='screen'
        )
    ])
```

**4. Build and Deploy the Package:**

After adding the new files, build your package and source the setup script:

```bash
colcon build --packages-select amigo_ros2_pi
source install/setup.bash
```

**5. Test the Service:**

Launch the service server using the launch file:

```bash
ros2 launch amigo_ros2_pi scan_controller_service_launch.py
```

In another terminal, call the service to run the `scan_controller_node.py`:

```bash
ros2 service call /run_scan_controller std_srvs/srv/Trigger
```

You should observe the `scan_controller_node.py` executing, and the service response will indicate its success or failure.

**Notes:**

- **Error Handling:** The service server includes basic error handling to manage exceptions and process errors.
- **Logging:** Both server and client nodes utilize ROS 2 logging to provide feedback on operations, aiding in debugging and monitoring.
- **Permissions:** Ensure that `scan_controller_node.py` has executable permissions. You can set this with:

  ```bash
  chmod +x path/to/scan_controller_node.py
  ```

By following these steps, you can integrate a ROS 2 service into your existing package to manage the execution of `scan_controller_node.py` upon request. 

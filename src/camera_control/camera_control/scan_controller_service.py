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

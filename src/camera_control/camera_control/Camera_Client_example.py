import rclpy
from rclpy.node import Node
from std_srvs.srv import Trigger

class ScanControllerClient(Node):
    def __init__(self):
        super().__init__('scan_controller_client')
        self.client = self.create_client(Trigger, 'run_scan_controller')
        while not self.client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for service to become available...')
        self.send_request()

    def send_request(self):
        request = Trigger.Request()
        self.future = self.client.call_async(request)
        self.future.add_done_callback(self.handle_response)

    def handle_response(self, future):
        try:
            response = future.result()
            if response.success:
                self.get_logger().info('scan_controller_node.py executed successfully.')
            else:
                self.get_logger().error(f'Execution failed: {response.message}')
        except Exception as e:
            self.get_logger().error(f'Service call failed: {str(e)}')

def main(args=None):
    rclpy.init(args=args)
    node = ScanControllerClient()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

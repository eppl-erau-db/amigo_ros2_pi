#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

class CameraScanNode(Node):
    def __init__(self):
        super().__init__('scan_controller_node')
        
        # Initialize the Motor Kit
        self.kit = MotorKit(i2c=board.I2C())
        
        # Setting a timer to perform a scan every 10 seconds 
        self.timer = self.create_timer(40.0, self.timer_callback)

        # Initializing tracking variables
        self.heading = 0
        self.pitch = 0
        self.heading_microsteps = 0
        self.pitch_microsteps = 0 
        self.angle_microstep = 1.8/16 # degrees

        # Scan positions (heading, pitch)
        self.scan_positions = [
            (-135, 0), (-135, 45), (-90, 45), (-90, 0),
            (-45, 0), (-45, 45), (0, 45), (0, 0),
            (45, 0), (45, 45), (90, 45), (90, 0),
            (135, 0), (135, 45), (0, 0)
        ]
        self.scan_index = 0

        # Timer for moving between scan positions every 0.5 seconds
        self.create_timer(2.0, self.next_scan_step)
            
    def timer_callback(self):
        """ Reset scan cycle when the timer triggers. """
        self.scan_index = 0  # Reset to start position
        
    def next_scan_step(self):
        """ Command the camera to the next position """
        if self.scan_index < len(self.scan_positions):
            target_heading, target_pitch = self.scan_positions[self.scan_index]
            self.move_camera(target_heading, target_pitch)
            self.scan_index += 1

    def move_camera(self, target_heading, target_pitch):

        if self.heading < target_heading:
            while self.heading != target_heading:
                self.heading_move_ccw()
        elif self.heading > target_heading:
            while self.heading != target_heading:
                self.heading_move_cw()

        if self.pitch < target_pitch:
            while self.pitch != target_pitch:
                self.pitch_move_ccw()
        elif self.pitch > target_pitch:
            while self.pitch != target_pitch:
                self.pitch_move_cw()

    def heading_move_ccw(self):
        self.heading_microsteps = self.kit.stepper1.onestep(style=stepper.INTERLEAVE, direction=stepper.FORWARD)
        self.heading = self.heading_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Heading:{self.heading}')

    def heading_move_cw(self):
        self.heading_microsteps = self.kit.stepper1.onestep(style=stepper.INTERLEAVE, direction=stepper.BACKWARD)
        self.heading = self.heading_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Heading:{self.heading}')

    def pitch_move_ccw(self):
        self.pitch_microsteps = self.kit.stepper2.onestep(style=stepper.INTERLEAVE, direction=stepper.FORWARD)
        self.pitch = self.pitch_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Pitch:{self.pitch}')
    
    def pitch_move_cw(self):
        self.pitch_microsteps = self.kit.stepper2.onestep(style=stepper.INTERLEAVE, direction=stepper.BACKWARD)
        self.pitch = self.pitch_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Pitch:{self.pitch}')
    
    def destroy(self):
        self.kit.stepper1.release()
        self.kit.stepper2.release()       
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = CameraScanNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

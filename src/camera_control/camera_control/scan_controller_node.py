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

        self.kit.stepper1 = stepper.StepperMotor()
        
        # Setting a timer to perform a scan every 20 seconds 
        self.timer_period = 20.0 
        self.timer = self.create_timer(self.timer_period, self.timer_callback)

        # Initializing tracking variables
        self.absolute_heading = 0
        self.absolute_pitch = 0
        self.heading_microsteps = 0
        self.pitch_microsteps = 0 
        self.angle_microstep = 1.8/16 # degrees
            
    def timer_callback(self):
        for i in range(100):
            self.heading_move_ccw()
        
    def heading_move_ccw(self):
        self.heading_microsteps = self.kit.stepper1.onestep(style=stepper.MICROSTEP, direction=stepper.FORWARD)
        self.absolute_heading = self.absolute_heading + self.heading_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Heading:{self.absolute_heading}')

    def heading_move_cw(self):
        self.heading_microsteps = self.kit.stepper1.onestep(style=stepper.MICROSTEP, direction=stepper.FORWARD)
        self.absolute_heading = self.absolute_heading - self.heading_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Heading:{self.absolute_heading}')

    def pitch_move_ccw(self):
        self.pitch_microsteps = self.kit.stepper2.onestep(style=stepper.MICROSTEP, direction=stepper.FORWARD)
        self.absolute_pitch = self.absolute_pitch + self.pitch_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Pitch:{self.absolute_pitch}')
    
    def pitch_move_cw(self):
        self.heading_microsteps = self.kit.stepper2.onestep(style=stepper.MICROSTEP, direction=stepper.FORWARD)
        self.absolute_pitch = self.absolute_heading + self.pitch_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Pitch:{self.absolute_pitch}')
    
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

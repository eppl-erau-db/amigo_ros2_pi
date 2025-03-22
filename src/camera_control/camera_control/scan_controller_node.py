#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
import board
from std_msgs.msg import Bool
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

class CameraScanNode(Node):
    def __init__(self):
        super().__init__('scan_controller_node')
        
        # Initialize the Motor Kit
        self.kit = MotorKit(i2c=board.I2C())
        
        # Setting a timer to perform a scan every 40 seconds 
        self.timer = self.create_timer(40.0, self.timer_callback)
        
        # Publisher for Image Taking
        self.publisher = self.create_publisher(Bool, '/take_picture', 10)
        
        # Initially setting to False
        self.msg = Bool()

        # Initializing tracking variables
        self.heading = 0
        self.pitch = 0
        self.heading_microsteps = 0
        self.pitch_microsteps = 0 
        self.angle_microstep = 1.8/16 # degrees

        # Scan positions (heading, pitch)
        self.scan_positions = [
            (-90, 45), (-90, 0),(-45, 0),
            (-45, 45), (0, 45), (0, 0),
            (45, 0), (45, 45), (90, 45), 
            (90, 0),(0, 0)]
        self.scan_index = 0
       	
        # Timer for moving between scan positions every 3.0 seconds
        self.create_timer(3.0, self.next_scan_step)
            
    def timer_callback(self):
        """ Reset scan cycle when the timer triggers. """
        # msg = Bool()
        
        # msg.data = True
        # self.publisher.publish(msg)
        # self.scan_index = 0  # Reset to start position
        
    def next_scan_step(self):
        """ Command the camera to the next position """  
        msg = Bool()

		# Go to the next Position           
        if self.scan_index < len(self.scan_positions):
            target_heading, target_pitch = self.scan_positions[self.scan_index]
            self.move_camera(target_heading, target_pitch)
            self.scan_index += 1

        time.sleep(1)
        msg.data = True
        self.publisher.publish(msg)
        time.sleep(0.5)
        msg.data = False
        self.publisher.publish(msg)

    def move_camera(self, target_heading, target_pitch):
        """ Move the camera to a target heading or target pitch """
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
        """ Move the camera heading counterclockwise """
        self.heading_microsteps = self.kit.stepper1.onestep(style=stepper.INTERLEAVE, direction=stepper.FORWARD)
        self.heading = self.heading_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Heading:{self.heading}')

    def heading_move_cw(self):
        """ Move the camera heading clockwise """
        self.heading_microsteps = self.kit.stepper1.onestep(style=stepper.INTERLEAVE, direction=stepper.BACKWARD)
        self.heading = self.heading_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Heading:{self.heading}')

    def pitch_move_ccw(self):
        """ Move the camera pitch counterclockwise """
        self.pitch_microsteps = self.kit.stepper2.onestep(style=stepper.INTERLEAVE, direction=stepper.FORWARD)
        self.pitch = self.pitch_microsteps * self.angle_microstep
        self.get_logger().info(f'The Current Absolute Pitch:{self.pitch}')
    
    def pitch_move_cw(self):
        """ Move the camera pitch clockwise """
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

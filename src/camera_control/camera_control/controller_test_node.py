#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

class StepperMotorNode(Node):
    def __init__(self):
        super().__init__('controller_test_node')
        
        # Initialize the Motor Kit
        self.kit = MotorKit(i2c=board.I2C())
        
        # Create timer with period of 5 seconds
        self.timer_period = 5.0 
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
    
    def timer_callback(self):
        self.move_motor_forward()
        self.move_motor_backward()

    def move_motor_forward(self):
        for i in range(100):
            self.kit.stepper1.onestep(style=stepper.SINGLE, direction=stepper.FORWARD)
            time.sleep(0.01)
        print("Stepper Motor 1 Moved FORWARD")
    
    def move_motor_backward(self):
        for i in range(100):
            self.kit.stepper2.onestep(style=stepper.SINGLE, direction=stepper.BACKWARD)
            time.sleep(0.01)
        print("Stepper Motor 2 Moved BACKWARD")
    
    def destroy(self):
        self.kit.stepper1.release()
        self.kit.stepper2.release()       
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    node = StepperMotorNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import RPi.GPIO as GPIO
from .DRV8825 import DRV8825

class StepperMotorNode(Node):
    def __init__(self):
        super().__init__('controller_test_node')
        
        # Initialize motors
        self.motor1 = DRV8825(dir_pin=13, step_pin=19, enable_pin=12, mode_pins=(16, 17, 20))
        self.motor2 = DRV8825(dir_pin=24, step_pin=18, enable_pin=4, mode_pins=(21, 22, 27))
        
        # Set both motors to full step
        self.motor1.SetMicroStep('software', 'fullstep')
        self.motor2.SetMicroStep('software', 'fullstep')
        
        # Timer to handle motor control
        self.timer = self.create_timer(4.0, lambda: self.move_motor_up(self.motor1))
    
    def move_motor_up(self, motor):
        motor.TurnStep(Dir='forward', steps=20, stepdelay=0.005)
        motor.Stop()
        print("Motor moved positive")
    
    def move_motor_down(self, motor):
        motor.TurnStep(Dir='backward', steps=2048, stepdelay=0.005)
        print("Motor moved negative")
    
    def destroy(self):
        self.motor1.Stop()
        self.motor2.Stop()
        GPIO.cleanup()
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
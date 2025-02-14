import time
import board
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

kit = MotorKit(i2c=board.I2C())

for i in range(1000):
	kit.stepper1.onestep(style=stepper.MICROSTEP)
	kit.stepper2.onestep(style=stepper.DOUBLE)
	#time.sleep(0.01)

kit.stepper1.release()
kit.stepper2.release()

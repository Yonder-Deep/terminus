"""
The motor_controller class calibrates and sets the speed of all of the motors
"""
import pigpio
from motor import Motor

LEFT_GPIO_PIN      = 4
RIGHT_GPIO_PIN     = 14
CENTER_GPIO_PIN    = 11

LEFT_MOTOR_INDEX   = 0
RIGHT_MOTOR_INDEX  = 1
CENTER_MOTOR_INDEX = 2
BALLAST            = 3

class MotorController:
    def __init__(self):
        """
        Initializes MotorController object and individual motor objects
        to respective gpio pins.
        """
        # Connection to Raspberry Pi GPIO ports.
        self.pi = pigpio.pi()

        # Motor object definitions.
        self.motor_pins = [LEFT_GPIO_PIN, RIGHT_GPIO_PIN, CENTER_GPIO_PIN]

        self.motors = [Motor(gpio_pin=pin, pi=self.pi) for pin in self.motor_pins]

    def update_motor_speeds(self, data):
        """
        Sets motor speeds to each individual motor.

        data: String read from the serial connection containing motor speed values.
        """
        self.motors[LEFT_MOTOR_INDEX].set_speed(data[LEFT_MOTOR_INDEX])
        
        self.motors[RIGHT_MOTOR_INDEX].set_speed(data[RIGHT_MOTOR_INDEX])
        
        self.motors[CENTER_MOTOR_INDEX].set_speed(data[CENTER_MOTOR_INDEX])

    def zero_out_motors(self):
        """
        Sets motor speeds of each individual motor to 0.
        """
        for motor in self.motors:
            motor.set_speed(0)

    def calibrate_motors(self):
        """
        Calibrates each individual motor.
        """
        for motor in self.motors:
            motor.calibrate_motor()

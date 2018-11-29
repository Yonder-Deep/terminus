"""
The motor_controller class calibrates and sets the speed of all of the motors
"""
import pigpio
from motor import Motor


class MotorController:
    def __init__(self, motor_config):
        """
        Initializes MotorController object and individual motor objects
        to respective gpio pins.

        motor_config: Dict of motor name to motor pin
        """
        # Connection to Raspberry Pi GPIO ports.
        self.pi = pigpio.pi()

        self.motors = {}

        # Motor object definitions.
        for name, pin in motor_config.items():
            self.motors[name] = Motor(gpio_pin=pin, pi=self.pi)

    def update_motor_speeds(self, data):
        """
        Sets motor speeds to each individual motor.

        data: Dict of motor name to motor speed read from the serial connection.
        """

        for name, speed in data.items():
            self.motors[name].set_speed(speed)

    def zero_out_motors(self):
        """
        Sets motor speeds of each individual motor to 0.
        """
        for motor in self.motors.values():
            motor.set_speed(0)

    def calibrate_motors(self):
        """
        Calibrates each individual motor.
        """
        for motor in self.motors.values():
            motor.calibrate_motor()

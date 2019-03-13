"""
The motor class calibrates and sets the speed of an individual motor.
"""
import time
import pigpio

CENTER_PWM_RANGE = 400
CENTER_PWM_VALUE = 1500
MAX_SPEED = 100

class Motor:
    def __init__(self, gpio_pin, pi):
        """
        Instantiate a motor.

        gpio_pin: Pin on Raspberry Pi that this motor is connected to.i
        pi:       Raspberry Pi GPIO object
        """
        self.pin = gpio_pin
        self.pi  = pi

    def set_speed(self, speed):
        """
        Sets the speed of the motor.

        speed: double value specifying the speed that the motor should be set to.
        """
        # Threshold for positive or negative speed.
        if speed > MAX_SPEED:
            speed -= MAX_SPEED
            speed *= -1

        # Conversion from received radio speed to PWM value.
        pwm_speed = speed * (CENTER_PWM_RANGE) / MAX_SPEED + CENTER_PWM_VALUE

        # Change speed of motor.
        self.pi.set_servo_pulsewidth(self.pin, pwm_speed)

    def calibrate_motor(self):
        """
        Calibrates the motor by setting speed values between time intervals.
        """
        self.set_speed(0)
        time.sleep(2)
        self.set_speed(MAX_SPEED / 2)
        time.sleep(2)
        self.set_speed(0)
        time.sleep (2)
        self.set_speed(0)
        time.sleep(2)
   #     time.sleep(1)

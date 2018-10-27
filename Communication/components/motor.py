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
        pi:         Raspberry Pi GPIO object
        """
        self.pin = gpio_pin
        self.pi  = pi

    def set_speed(self, speed):
        # Threshold for positive or negative speed.
        if speed > MAX_SPEED:
            speed -= MAX_SPEED
            speed *= -1

        # Conversion from received radio speed to PWM value.
        pwm_speed = speed * (CENTER_PWM_RANGE) / MAX_SPEED + CENTER_PWM_VALUE

        # Change speed of motor.
        self.pi.set_servo_pulsewidth(self.pin, pwm_speed)

    def calibrate_motor(self):
        self.set_speed(0)
        time.sleep(2)
        self.set_speed(MAX_SPEED / 2)
        time.sleep(2)
        self.set_speed(0)
        time.sleep (2)
        self.set_speed(0)
        time.sleep(2)

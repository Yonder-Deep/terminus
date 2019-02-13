"""
The motor_controller class calibrates and sets the speed of all of the motors
"""
import pigpio
from motor import Motor
import RPi.GPIO as io
LEFT_GPIO_PIN   = 4  #18
RIGHT_GPIO_PIN  = 11 #24
FRONT_GPIO_PIN  = 18 #4
BACK_GPIO_PIN   = 24 #11

#Define pin numbers for PI
LEFT_PI_PIN  = 7
RIGHT_PI_PIN = 23
FRONT_PI_PIN = 12
BACK_PI_PIN  = 18


LEFT_MOTOR_INDEX   = 0
RIGHT_MOTOR_INDEX  = 1
FRONT_MOTOR_INDEX  = 2
BACK_MOTOR_INDEX   = 3
BALLAST            = 4

class MotorController:
    def __init__(self):
        """
        Initializes MotorController object and individual motor objects
        to respective gpio pins.
        """
        # Connection to Raspberry Pi GPIO ports.
        self.pi = pigpio.pi()

        # Motor object definitions.
        self.motor_pins = [LEFT_GPIO_PIN, RIGHT_GPIO_PIN, FRONT_GPIO_PIN, BACK_GPIO_PIN]
        self.pi_pins = [LEFT_PI_PIN, 23, 12, 18]

        self.motors = [Motor(gpio_pin=pin, pi=self.pi) for pin in self.motor_pins]

#        self.check_gpio_pins()

    def update_motor_speeds(self, data):
        """
        Sets motor speeds to each individual motor.

        data: String read from the serial connection containing motor speed values.
        """
 #       print("Setting Left Motor to ", data[LEFT_MOTOR_INDEX] )
        self.motors[LEFT_MOTOR_INDEX].set_speed(data[LEFT_MOTOR_INDEX])
  #      print("Setting Right Motor to ", data[RIGHT_MOTOR_INDEX])
        self.motors[RIGHT_MOTOR_INDEX].set_speed(data[RIGHT_MOTOR_INDEX])
   #     print("Setting Front and Back Motor to ", data[FRONT_MOTOR_INDEX])
        self.motors[FRONT_MOTOR_INDEX].set_speed(data[FRONT_MOTOR_INDEX])
        self.motors[BACK_MOTOR_INDEX].set_speed(data[FRONT_MOTOR_INDEX])

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
        ct = 0
        for motor in self.motors:
            ct += 1
        #    print("Inside calibrating_motors for loop")
            print("Calibrating motor ", ct)
            #try:
            motor.calibrate_motor()
            #except AttributeError as err:
              #  print("Caught error calibrating motors: ", err)
             #   continue
    def check_gpio_pins(self):
        io.setmode(io.BOARD)
        for pins in self.pi_pins:
            io.setup(pins, io.IN)
            print("Pin:", pins, io.input(pins))


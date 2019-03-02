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

MAX_CORRECTION_MOTOR_SPEED = 25 # Max turning speed during pid correction


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

        self.left_speed = 0
        self.right_speed = 0
        self.front_speed = 0
        self.back_speed = 0
#        self.check_gpio_pins()

    def update_motor_speeds(self, data):
        """
        Sets motor speeds to each individual motor.

        data: String read from the serial connection containing motor speed values.
        """
 #       print("Setting Left Motor to ", data[LEFT_MOTOR_INDEX] )

        # Parse motor speed from radio
        self.left_speed = data[LEFT_MOTOR_INDEX]
        self.right_speed = data[RIGHT_MOTOR_INDEX]
        self.front_speed = data[FRONT_MOTOR_INDEX]
        self.back_speed = data[FRONT_MOTOR_INDEX]

        # Set motor speed
        self.motors[LEFT_MOTOR_INDEX].set_speed(self.left_speed)
  #      print("Setting Right Motor to ", data[RIGHT_MOTOR_INDEX])
        self.motors[RIGHT_MOTOR_INDEX].set_speed(self.right_speed)
   #     print("Setting Front and Back Motor to ", data[FRONT_MOTOR_INDEX])
        self.motors[FRONT_MOTOR_INDEX].set_speed(self.front_speed)
        self.motors[BACK_MOTOR_INDEX].set_speed(self.back_speed)

    def pid_motor(self, pid_feedback):
        """
        Updates left and right motor speed base off pid feedback
        
        feedback: Feedback value from pid class.
        """ 
        self.left_speed = self.calculate_pid_new_speed(self.left_speed, pid_feedback)
        self.right_speed = self.calculate_pid_new_speed(self.right_speed, - pid_feedback)
        print("[PID_MOTOR]\t" + str(self.left_speed) + "\t" + str(self.right_speed))
        self.motors[LEFT_MOTOR_INDEX].set_speed(self.left_speed)
        self.motors[RIGHT_MOTOR_INDEX].set_speed(self.right_speed)
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


    def calculate_pid_new_speed(self, last_speed, speed_change):
        #print(">>Last speed\t" + str(last_speed) + "speed_change\t" + str(speed_change))
        #new_speed = last_speed + speed_change
        # Case 1: was going forward
        assert(not (MAX_CORRECTION_MOTOR_SPEED < last_speed and last_speed <= 100)), "Unexpected last speed" + str(last_speed) 
        assert(not (100 + MAX_CORRECTION_MOTOR_SPEED < last_speed and last_speed <= 200)), "Unexpected last speed" + str(last_speed)
        if(last_speed <= MAX_CORRECTION_MOTOR_SPEED):
            new_speed = last_speed + speed_change
            lower_speed_cap = 0
            upper_speed_cap = MAX_CORRECTION_MOTOR_SPEED
        # Case 2: was going backward
        else:
            new_speed = last_speed - speed_change
            lower_speed_cap = 100
            upper_speed_cap = 100 + MAX_CORRECTION_MOTOR_SPEED


        # Exceed speed range, too big
        if(new_speed > upper_speed_cap):
            new_speed = upper_speed_cap
        # Exceed, too small
        if(new_speed < lower_speed_cap):
            
            # Was going forward, want to backward
            if(last_speed <= MAX_CORRECTION_MOTOR_SPEED):
                #print("Adjust case forward -> backward")
                new_speed = abs(new_speed) + 100
                # if it goes backward too fast
                if(new_speed > 100 + MAX_CORRECTION_MOTOR_SPEED):
                    new_speed = 100 + MAX_CORRECTION_MOTOR_SPEED
            else: # was going backward, want to forward
                #print("Adjust case backward -> forward")
                new_speed = 100 - new_speed
                # if it goes forward too fast
                if(new_speed > MAX_CORRECTION_MOTOR_SPEED):
                    new_speed = MAX_CORRECTION_MOTOR_SPEED

        assert(not (MAX_CORRECTION_MOTOR_SPEED < new_speed and new_speed <= 100)), "Unexpected new speed output" + str(new_speed)
        assert(not (100 + MAX_CORRECTION_MOTOR_SPEED < new_speed and new_speed <= 200)), "Unexpected new speed output" + str(new_speed)
        return new_speed

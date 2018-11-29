import math


class NavController:
    def __init__(self, joy, debug=False):
        self.joy = joy
        self.state = None
        self.turnSpeed = 50
        self.motorIncrements = 8
        self.maxSpeed = 100
        self.debug = debug

    def get_packet(self):
        motor_speed_right = 0
        motor_speed_left = 0
        motor_speed_base = 0

        # In place turn. If right bumper clicked, motors adjust
        if self.joy.rightBumper():
                right_stick_value = math.floor(self.joy.rightX() * self.motorIncrements) / self.motorIncrements
                motor_speed_right = int(self.turnSpeed * (-right_stick_value))
                motor_speed_left = int(self.turnSpeed * right_stick_value)
        else:
                if self.joy.rightTrigger() > 0:
                    motor_speed_base = int(self.joy.rightTrigger()*self.maxSpeed)
                else:
                    motor_speed_base = int(-1*self.joy.leftTrigger() * self.maxSpeed)

                left_stick_value = math.floor( ( (self.joy.leftX() + 1 ) / 2) * self.motorIncrements) / self.motorIncrements
                motor_speed_left = int(left_stick_value * motor_speed_base)
                motor_speed_right = int((1 - left_stick_value) * motor_speed_base)

        if motor_speed_left < 0:
            motor_speed_left *= -1
            motor_speed_left += 100

        if  motor_speed_right < 0:
            motor_speed_right *= -1
            motor_speed_right += 100

        if motor_speed_base < 0:
            motor_speed_base *= -1
            motor_speed_base += 100

        if self.debug:
            print("Base motor ", str(motor_speed_base))
            print("Left motor ", str(motor_speed_left))
            print("Right motor ", str(motor_speed_right))

        ballast = self.joy.B()

        speed_f = chr(motor_speed_left) + chr(motor_speed_right) + chr(ballast) + '\n'

        return speed_f


#TODO
# REMOVE MOTOR SPEED BASE

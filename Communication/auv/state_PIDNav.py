from __future__ import print_function
from state import State
import time

GPS_TIMEOUT_KILL_TIME = 10

class PIDNav(State):
    def __init__(self, auv):
        self.l_speed = 0
        self.r_speed = 0
        self.f_speed = 0
        self.b_speed = 0
        self.last_control_time = time.time()
        assert auv.mc, 'Motor controller not initialized'
        assert auv.gps_info, 'GPS info not available'
        self.mc = auv.mc
        self.handle(auv)

    def handle(self, auv):
        state_data = auv.state_info['data']
        if 'l' in state_data:
            self.last_control_time = time.time()
            left = state_data['l']
            right = state_data['r']
            front = state_data['f']
            back = state_data['b']
            self.update_speed(left, right, front, back)
        # print(str(auv.state_info))

        # Reach set point
        # TODO

        # GPS timeout
        if time.time() - auv.gps_info['updated'] > GPS_TIMEOUT_KILL_TIME:
            print("PID control timed out")
            self.zero_motors()

        return {'hold_state': 'NAV',
                'next_state': 'READ',
                'data': dict()}

    def zero_motors(self):
        self.l_speed = 0
        self.r_speed = 0
        self.f_speed = 0
        self.b_speed = 0
        self.set_speed()

    def update_speed(self, left, right, front, back):
        if all([left == self.l_speed, right == self.r_speed, front == self.f_speed, back == self.b_speed]):
            return  # Do nothing if speed unchanged
        else:
            self.l_speed = left
            self.r_speed = right
            self.f_speed = front
            self.b_speed = back
            self.set_speed()

    def set_speed(self):
        print("[NAV]", self.l_speed, self.r_speed, self.f_speed, self.b_speed, end='')
        self.mc.update_motor_speeds(self.l_speed, self.r_speed, self.f_speed, self.b_speed)

    def get_state_name(self):
        return 'PID Navigate'

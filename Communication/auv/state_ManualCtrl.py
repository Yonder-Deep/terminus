from __future__ import print_function
from state import State
import time

MANUAL_CONTROL_TIMEOUT_SECONDS = 0.5


class ManualCtrl(State):
    def __init__(self, auv):
        self.l_speed = 0
        self.r_speed = 0
        self.f_speed = 0
        self.b_speed = 0
        self.last_control_time = time.time()
        self.handle(auv)

    def handle(self, auv):
        assert auv.mc, 'Motor controller not initialized'
        state_data = auv.state_info['data']
        if 'l' in state_data:
            self.last_control_time = time.time()
            left = state_data['l']
            right = state_data['r']
            front = state_data['f']
            back = state_data['b']
            self.update_speed(left, right, front, back)
        # print(str(auv.state_info))

        # Control timeout
        if time.time() - self.last_control_time > MANUAL_CONTROL_TIMEOUT_SECONDS:
            print("Manual control timed out")
            self.zero_motors()
            return {'hold_state': 'READ',
                    'next_state': 'READ',
                    'data': dict()}

        return {'hold_state': 'MAN',
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
        print("[MAN]", self.l_speed, self.r_speed, self.f_speed, self.b_speed, end='')
        # TODO: call mc to actually set motors

    def get_state_name(self):
        return 'MAN'

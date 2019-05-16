from __future__ import print_function
from state import State

class ManualCtrl(State):
    def __init__(self, auv):
        self.handle(auv)
        self.l_speed = 0
        self.r_speed = 0
        self.f_speed = 0
        self.b_speed = 0

    def handle(self, auv):
        assert auv.mc, 'Motor controller not initialized'
        state_data = auv.state_info['data']
        if 'l' in state_data:
            self.l_speed = state_data['l']
            self.r_speed = state_data['r']
            self.f_speed = state_data['f']
            self.b_speed = state_data['b']
        print("[MAN]", self.l_speed, self.r_speed, self.f_speed, self.b_speed, end='')
        # print(str(auv.state_info))
        return {'hold_state': 'MAN',
                'next_state': 'READ',
                'data': dict()}

    def get_state_name(self):
        return 'MAN'

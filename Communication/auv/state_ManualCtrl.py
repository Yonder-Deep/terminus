from __future__ import print_function
from state import State

class ManualCtrl(State):
    def __init__(self, auv):
        self.handle(auv)

    def handle(self, auv):
        assert auv.mc, 'Motor controller not initialized'
        hold_state = auv.state_info['hold_state']
        state_data = auv.state_info['data']
        left_motor = state_data['l']
        right_motor = state_data['r']
        front_motor = state_data['f']
        back_motor = state_data['b']
        print("[MAN]", left_motor, right_motor, front_motor, back_motor, end='')
        auv.mc
        # print(str(auv.state_info))
        return {'hold_state': hold_state,
                'next_state': 'READ',
                'data': dict()}

    def get_state_name(self):
        return 'MAN'

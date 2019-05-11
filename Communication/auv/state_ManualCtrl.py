from state import State


class ManualCtrl(State):
    def __init__(self, auv):
        self.handle(auv)

    def handle(self, auv):
        assert auv.mc, 'Motor controller not initialized'
        state_before_read = auv.state_info['last_state']
        state_data = auv.state_info['data']
        left_motor = state_data['l']
        right_motor = state_data['r']
        front_motor = state_data['f']
        back_motor = state_data['b']
        print("[MAN]", left_motor, right_motor, front_motor, back_motor)
        print(str(auv.state_info))
        return {'last_state': 'READ',
                'next_state': state_before_read,
                'data': dict()}

    def get_state_name(self):
        return 'MAN'
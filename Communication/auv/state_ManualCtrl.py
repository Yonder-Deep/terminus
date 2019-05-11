from state import State


class ManualCtrl(State):
    def __init__(self, auv):
        self.handle(auv)

    def handle(self, auv):
        state_before_read = auv.next_state['last_state']
        print(str(auv.next_state))
        return {'last_state': 'READ',
                'next_state': state_before_read,
                'data': dict()}

    def get_state_name(self):
        return 'MAN'

from state import State


class WaitForAction(State):
    def __init__(self, auv):
        print('Waiting for GUI command')

    def handle(self, auv):
        print('Waiting for action.')
        return {'last_state': auv.next_state['last_state'],
                'next_state': 'WAIT',
                'data': dict()}

    def get_state_name(self):
        return 'INIT'

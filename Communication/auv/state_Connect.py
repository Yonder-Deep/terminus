from state import State


class Connect(State):
    def __init__(self):
        print('Waiting for Radio Connection')

    def handle(self, auv):
        raise NotImplementedError('INIT states shouldn\'t be called as next state')

    def get_state_name(self):
        return 'INIT'

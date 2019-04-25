from state import State


class WaitForAction(State):
    def __init__(self, auv):
        print('Waiting for GUI command')

    def handle(self, auv):
        raise NotImplementedError()

    def get_state_name(self):
        return 'INIT'

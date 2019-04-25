from state import State


class ReadRadio(State):
    def __init__(self, auv):
        print('Reading from Radio')

    def handle(self, auv):
        raise NotImplementedError('INIT states shouldn\'t be called as next state')

    def get_state_name(self):
        return 'ReadRadio'

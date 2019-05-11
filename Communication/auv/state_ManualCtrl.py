from state import State


class ManualCtrl(State):
    def __init__(self, auv):
        self.handle(auv)

    def handle(self, auv):
        print(str(auv.next_state))

    def get_state_name(self):
        return 'MAN'

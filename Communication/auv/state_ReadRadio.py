from state import State


class ReadRadio(State):
    def __init__(self, auv):
        assert auv.radio
        assert auv.radio.is_open()

    def handle(self, auv):
        state_before_read = auv.next_state['last_state']
        next_state = 'WAIT'  # FIXME: Pass this to command handler and get next state name
        return {'last_state': 'READ',
                'next_state': next_state,
                'data': dict()}

    def get_state_name(self):
        return 'ReadRadio'

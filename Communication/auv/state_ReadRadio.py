from state import State
import command_router

class ReadRadio(State):
    def __init__(self, auv):
        assert auv.radio
        assert auv.radio.is_open()

    def handle(self, auv):
        command = auv.radio.read()
        if command:
            return command_router.parse_command(auv.next_state, command)
        else:
            state_before_read = auv.next_state['last_state']
            return {'last_state': 'READ',
                    'next_state': state_before_read,
                    'data': dict()}

    def get_state_name(self):
        return 'ReadRadio'

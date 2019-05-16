from state import State
import command_router

class ReadRadio(State):
    def __init__(self, auv):
        assert auv.radio
        assert auv.radio.is_open()

    def handle(self, auv):
        command = auv.radio.read()
        if command:
            print("Handling command>>")
            foo = command_router.parse_command(auv.state_info, command)
            # print("ReadRadio returning ->" + str(foo) + "<-")
            return foo
        else:
            hold_state = auv.state_info['hold_state']
            return {'hold_state': hold_state,
                    'next_state': hold_state,
                    'data': dict()}

    def get_state_name(self):
        return 'ReadRadio'

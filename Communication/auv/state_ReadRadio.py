from __future__ import print_function
from state import State
import command_router
import time


class ReadRadio(State):
    def __init__(self, auv):
        assert auv.radio
        assert auv.radio.is_open()
        auv.last_connect = time.time()

    def handle(self, auv):
        if 'delete_state' in auv.state_info['data'].keys():
            state_to_delete = auv.state_info['data']['delete_state']
            assert state_to_delete in auv.states.keys()
            auv.states.pop(state_to_delete)

        print('[COMM] Last Connect:' + str(time.time() - auv.last_connect))
        command = auv.radio.read()
        if command:
            # print("Handling command>>")
            next_state_info = command_router.parse_command(auv.state_info, command)
            # print("ReadRadio returning ->" + str(foo) + "<-")
            return next_state_info
        else:
            hold_state = auv.state_info['hold_state']
            return {'hold_state': hold_state,
                    'next_state': hold_state,
                    'data': dict()}

    def get_state_name(self):
        return 'ReadRadio'

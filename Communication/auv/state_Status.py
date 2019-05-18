from state import State
import time


class Status(State):
    def __init__(self, auv):
        assert auv.radio
        assert auv.radio.is_open()
        assert auv.command
        self.handle(auv)

    def handle(self, auv):
        auv.last_connect = time.time()
        hold_state = auv.state_info['hold_state']
        auv.command.send_status(current_lat=10, current_lon=10, current_state=hold_state)
        return {'hold_state': hold_state,
                'next_state': hold_state,
                'data': dict()}

    def get_state_name(self):
        return 'Status'

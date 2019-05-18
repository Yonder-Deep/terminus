from state import State
import time


class Ballast(State):
    def __init__(self, auv):
        self.target_depth = auv.state_info['data']['depth']
        self.timeout = auv.state_info['data']['timeout']
        self.start_time = time.time()
        self.mc.update_motor_speeds(left=0, right=0, front=0, back=0)

    def handle(self, auv):
        current_depth = auv.pressure_sensor.depth()
        if current_depth < self.target_depth:
            # Continue ballasting
            pass
        hold_state = auv.state_info['hold_state']
        return {'hold_state': hold_state,
                'next_state': hold_state,
                'data': dict()}

    def get_state_name(self):
        return 'Ballast'

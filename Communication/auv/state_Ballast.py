from state import State
import time

BALLAST_SPEED = 25


class Ballast(State):
    def __init__(self, auv):
        self.target_depth = auv.state_info['data']['depth']
        self.timeout = auv.state_info['data']['timeout']
        self.start_time = time.time()
        self.mc.update_motor_speeds(left=0, right=0, front=BALLAST_SPEED, back=BALLAST_SPEED)

    def handle(self, auv):
        current_depth = auv.pressure_sensor.depth()
        if current_depth < self.target_depth:
            print("[BAL] At depth " + str(current_depth))
            hold_state = auv.state_info['hold_state']
            return {'hold_state': 'BAL',
                    'next_state': 'READ',
                    'data': dict()}

        elif current_depth >= self.target_depth:
            # End ballasting
            print("Done ballasting")

        elif time.time() - self.start_time > self.timeout:
            print("[BAL] TIME OUT!!")
            # TODO: If the depth doesn't change by 1m for 10s, reverse motor to come back up

        # BAL state done
        self.mc.update_motor_speeds(left=0, right=0, front=0, back=0)
        return {'hold_state': 'READ',
                'next_state': 'READ',
                'data': dict()}

    def get_state_name(self):
        return 'Ballast'

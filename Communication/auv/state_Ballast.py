from state import State
import time

BALLAST_SPEED = 25


class Ballast(State):
    def __init__(self, auv):
        print("Initializing ballasting")
        assert auv.pressure_sensor
        self.target_depth = auv.state_info['data']['depth']
        self.timeout = auv.state_info['data']['timeout']
        self.start_time = time.time()
        auv.mc.update_motor_speeds(left=0, right=0, front=BALLAST_SPEED, back=BALLAST_SPEED)

    def handle(self, auv):
        current_depth = auv.pressure_sensor.depth()

        # # TODO: Remove this: for debug use
        # current_depth = time.time() - self.start_time

        if current_depth >= self.target_depth:
            # End ballasting
            print("Done ballasting")

        elif (time.time() - self.start_time) > self.timeout:
            print("[BAL] TIME OUT!!")
            # TODO: If the depth doesn't change by 1m for 10s, reverse motor to come back up

        elif current_depth < self.target_depth:
            print("[BAL] At depth " + str(current_depth))
            return {'hold_state': 'BAL',
                    'next_state': 'READ',
                    'data': dict()}

        # BAL state done
        auv.mc.update_motor_speeds(left=0, right=0, front=0, back=0)
        return {'hold_state': 'READ',
                'next_state': 'READ',
                'data': {'delete_state': 'BAL'}}

    def get_state_name(self):
        return 'Ballast'

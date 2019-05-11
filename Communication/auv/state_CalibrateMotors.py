from state import State
import os
import sys

# Sets the PYTHONPATH to include the components.
split_path = os.path.abspath(__file__).split('/')
split_path_communication = split_path[0:len(split_path) - 2]
components_path = "/".join(split_path_communication) + "/components"
sys.path.append(components_path)

from motor_controller import MotorController


class CalibrateMotors(State):
    def __init__(self, auv):
        auv.mc = MotorController()
        self.handle(auv)

    def handle(self, auv):
        assert auv.mc, 'Motor controller not initialized'
        state_before_read = auv.state_info['last_state']
        state_data = auv.state_info['data']
        if state_data['l']: auv.mc.calibrate_left()
        if state_data['r']: auv.mc.calibrate_right()
        if state_data['f']: auv.mc.calibrate_front()
        if state_data['b']: auv.mc.calibrate_back()
        return {'last_state': 'CAL',
                'next_state': state_before_read,
                'data': dict()}

    def get_state_name(self):
        return 'CAL'

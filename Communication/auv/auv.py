import logging
import os
import sys
import time

import state_Connect
import state_InitSensors
import state_ReadRadio
import state_ManualCtrl
import state_CalibrateMotors

# Configure Logging
log_file_name = "mylog"
if not os.path.exists("log/"):
    os.makedirs("log/")

logger = logging.getLogger('AUV_Root')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler("log/{0}.log".format(log_file_name))
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

AUV_STATES = {
    'INIT': (state_InitSensors.InitSensors, 'CONNECT'),
    'CONNECT': (state_Connect.Connect, 'READ'),
    'READ': (state_ReadRadio.ReadRadio, 'READ'),
    'MAN': (state_ManualCtrl.ManualCtrl, 'READ'),
    'CAL': (state_CalibrateMotors.CalibrateMotors, 'READ')
}


class AUV():
    def __init__(self):
        self.radio = None  # Will be initialized in INIT state
        self.always_listen = False  # Flag to mark constant pulling from radio
        logger.debug("AUV Initializing")
        self.states = dict()
        self.state_info = {'hold_state': 'READ', 'next_state': 'INIT'}
        self.sensors = None
        self.mc = None
        self.run_state('INIT')
        logger.info("AUV Started")

    def add_state(self, adding_state):
        assert adding_state not in self.states.keys(), 'Cannot add ' + adding_state.get_state_name() + 'that already exist in state list!'
        assert adding_state in AUV_STATES.keys(), 'State ' + adding_state + ' not found!'
        self.states[adding_state] = AUV_STATES[adding_state][0](self)
        self.state_info['next_state'] = AUV_STATES[adding_state][1]

    def run_forever(self):
        while True:
            # time.sleep(0.1)
            self.run_state(self.state_info['next_state'])

    def run_state(self, state_name):
        if state_name not in self.states.keys():
            logger.debug("Init state >> " + state_name)
            self.add_state(state_name)
        else:
            logger.debug("State >> " + state_name)
            self.state_info = self.states[state_name].handle(self)
            # print(str(self.state_info))


if __name__ == '__main__':
    auv = AUV()
    try:
        auv.run_forever()
    except Exception as e:
        # TODO: Clean up motors and stuff
        logger.error("AUV_Root returns uncaught Error!!", exc_info=True)

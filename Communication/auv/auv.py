import state
import sensors
import logging
import os
import sys

import state_Connect
import state_InitSensors
import state_ReadRadio
import state_WaitForAction

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
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
logger.addHandler(ch)
logger.addHandler(fh)

AUV_STATES = {
    'CONNECT': (state_Connect.Connect, 'INIT'),
    'INIT': (state_InitSensors.InitSensors, 'READ'),
    'READ': (state_ReadRadio.ReadRadio, 'WAIT'),
    'WAIT': (state_WaitForAction.WaitForAction, 'READ')
}


class AUV():
    def __init__(self):
        self.radio = None  # Will be initialized in INIT state
        self.always_listen = False  # Flag to mark constant pulling from radio
        logger.debug("AUV Initializing")
        self.states = dict()
        self.next_state = {'last_state': 'INIT', 'next_state': 'INIT'}
        self.sensors = None
        logger.info("AUV Started")

    def next_state_is_read_radio(self):
        """ Generator that yields an on off for radio"""
        read = False
        while True:
            read = not read
            yield read

    def add_state(self, adding_state):
        assert adding_state not in self.states.keys(), 'Cannot add ' + adding_state.get_state_name() + 'that already exist in state list!'
        assert adding_state in AUV_STATES.keys(), 'State ' + adding_state + ' not found!'
        self.states[adding_state] = AUV_STATES[adding_state][0](self)
        self.next_state['next_state'] = AUV_STATES[adding_state][1]

    def run_forever(self):
        read_radio = self.next_state_is_read_radio()
        while True:
            if next(read_radio):
                self.run_state(self.next_state['next_state'])
            else:
                self.run_state('READ')

    def run_state(self, state_name):
        if state_name not in self.states.keys():
            logger.debug("Init state >> " + state_name)
            self.add_state(state_name)
        else:
            logger.debug("State >> " + state_name)
            self.next_state = self.states[state_name].handle(self)


if __name__ == '__main__':
    auv = AUV()
    try:
        auv.run_forever()
    except Exception as e:
        # TODO: Clean up motors and stuff
        logger.error("AUV_Root returns uncaught Error!!", exc_info=True)

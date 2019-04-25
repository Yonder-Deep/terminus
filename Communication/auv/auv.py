import state
import sensors
import logging
import os
import sys

import state_Connect
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
    'INIT': (state_Connect.Connect, 'CONNECT')
}


class AUV():
    def __init__(self):
        logger.debug("AUV Initializing")
        self.states = dict()
        self.next_state = 'INIT'
        self.sensors = None
        logger.info("AUV Started")

    def add_state(self, adding_state):
        assert adding_state not in self.states.keys(), 'Cannot add ' + adding_state.get_state_name() + 'that already exist in state list!'
        assert adding_state in AUV_STATES.keys(), 'State ' + adding_state + ' not found!'
        self.states[adding_state] = AUV_STATES[adding_state][0](self)
        self.next_state = AUV_STATES[adding_state][1]

    def run_forever(self):
        while True:
            if self.next_state not in self.states.keys():
                self.add_state(self.next_state)
            else:
                self.next_state = self.states[self.next_state].handle(self)


if __name__ == '__main__':
    auv = AUV()
    try:
        auv.run_forever()
    except Exception as e:
        logger.error("AUV_Root returns uncault Error!!", exc_info=True)

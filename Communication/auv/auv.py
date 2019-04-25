import state
import sensors
import logging, sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO)

filehandler = logging.FileHandler('mylog.log')
formatter = logging.Formatter("%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s") # set format

logging.debug("debug message") # no output
logging.info("info message")
logging.error("error")


class AUV():
    def __init__(self):
        self.states = dict()
        self.next_state = 'INIT'
        self.sensors = None
        logging.info('AUV Started')

    def add_state(self, adding_state):
        assert adding_state.get_state_name() not in self.states.keys(), 'Cannot add ' + adding_state.get_state_name() + 'that already exist in state list!'

    def run_forever(self):
        while True:
            self.next_state = self.states[self.next_state].handle(self)
            if self.next_state not in self.states.keys():
                self.add_state(self.next_state)


if __name__ == '__main__':
    auv = AUV(debug=True)
    try:
        auv.run_forever()
    except:
        print('Exception!')

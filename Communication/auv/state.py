from abc import ABCMeta, abstractmethod
import state_Connect
import state_WaitForAction

class State:
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self):
        raise NotImplementedError('State must override method __init__!')

    @abstractmethod
    def handle(self, auv):
        raise NotImplementedError('State must override method handle!')

    @abstractmethod
    def get_state_name(self):
        raise NotImplementedError('State must override method get_state_name!')
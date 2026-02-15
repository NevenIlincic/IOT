from enum import Enum
from enums import State
    
class SecuritySystem(object):
    def __init__(self):
        self.value = State.OFF
    
    def change_state(self):
        pass
from enum import Enum

class DoorLightState(Enum):
    ON = 1
    OFF = 0
    
class Buzzing(Enum):
    BUZZING = 1
    STOPPED = 0

class State(Enum):
    ON = 1
    OFF = 0

class DoorState(Enum):
    OPEN = 1
    CLOSED = 0
    
class Attempt(Enum):
    SUCCESS = 1
    FAIL = 0

class AlarmState(Enum):
    ACTIVE = 1
    NOT_ACTIVE = 0
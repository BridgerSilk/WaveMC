from enum import Enum

class State(Enum):
    handshake = 0
    status = 1
    login = 2
    play = 3
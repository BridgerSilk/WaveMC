import struct
from net.io import *
from packets.packetmap import *
from enums.state import *

class TimeUpdate:
    def __init__(self, world_age, time):
        self.id = packetmap_client[State.play.value]["time_update"]
        self.packet = struct.pack(">qq", world_age, time)

        # world_age: long
        # time: long
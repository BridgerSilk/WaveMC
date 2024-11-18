import struct
from net.io import *
from packets.packetmap import *
from enums.state import *

class HeldItemChange:
    def __init__(self, slot):
        self.id = packetmap_client[State.play.value]["held_item_change"]
        self.packet = struct.pack("b", slot)

        # slot: byte

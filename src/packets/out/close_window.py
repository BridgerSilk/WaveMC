import struct
from net.io import *
from packets.packetmap import *
from enums.state import *

class CloseWindow:
    def __init__(self, win):
        self.id = packetmap_client[State.play.value]["close_window"]
        self.packet = struct.pack(">B", win)

        # win: unsigned byte
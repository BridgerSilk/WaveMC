import struct
from net.io import *
from packets.packetmap import *
from enums.state import *

class PlayerPositionAndLook:
    def __init__(self, x, y, z, yaw, pitch, flags):
        self.id = packetmap_client[State.play.value]["player_pos_and_look"]
        self.packet = struct.pack(">dddffb", x, y, z, yaw, pitch, flags)

        # x: double
        # y: double
        # z: double
        # yaw: float
        # pitch: float
        # flags: byte

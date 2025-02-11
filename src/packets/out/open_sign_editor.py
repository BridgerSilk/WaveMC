import struct
from net.io import *
from packets.packetmap import *
from enums.state import *
from buffer.write_buffer import *
from utils.encode_pos import *

class OpenSignEditor:
    def __init__(self, x, y, z):
        self.id = packetmap_client[State.play.value]["open_sign_editor"]
        self.packet = encode_position(x, y, z)
import struct
from net.io import *
from packets.packetmap import *
from enums.state import *
from buffer.write_buffer import *

class UpdateHealth:
    def __init__(self, health, food, foodsaturation):
        self.id = packetmap_client[State.play.value]["update_health"]
        self.parts = []
        self.parts.append(struct.pack(">f", health))
        self.parts.append(write_varint(food))
        self.parts.append(struct.pack(">f", foodsaturation))
        self.packet = b''.join(self.parts)

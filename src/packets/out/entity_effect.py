import struct
from net.io import *
from packets.packetmap import *
from enums.state import *
from buffer.write_buffer import *

# fix - doesnt work (game crashes when joining)
# now doesnt crash anymore, but still doesnt work

class EntityEffect:
    def __init__(self, entityid, effectid, amplifier, duration, hideparticles):
        self.id = packetmap_client[State.play.value]["entity_effect"]
        self.part1 = struct.pack("bb", effectid, amplifier)
        self.part2 = struct.pack("?", hideparticles)
        self.part3 = write_varint(entityid)
        self.part4 = write_varint(duration)
        self.parts = [self.part1, self.part2, self.part3, self.part4]
        self.packet = b''.join(self.parts)

        # entityid: varint
        # effectid: byte
        # amplifier: byte
        # duration: varint
        # hideparticles: boolean
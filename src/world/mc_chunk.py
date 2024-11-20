import struct
import zlib
from buffer.write_buffer import *
from io import BytesIO
from net.io import *

def write_varint(value):
    result = b""
    while value > 0x7F:
        result += struct.pack("B", (value & 0x7F) | 0x80)
        value >>= 7
    result += struct.pack("B", value & 0x7F)
    return result

class Chunk:
    SECTIONS = 16

    def __init__(self, x, z):
        self.x = x
        self.z = z
        self.sections = [ChunkSection(i) for i in range(Chunk.SECTIONS)]
        self.x_absolute = x * 16
        self.z_absolute = z * 16

    def get_section_from_y(self, y):
        return self.sections[y // 16]
    
    def set_block_at(self, x, y, z, block_data):
        section = self.get_section_from_y(y)
        section.set_block_at_relative(x, y, z, block_data)

    def send_chunk_data(self, conn):
        chunk_coords = struct.pack(">ii", self.x, self.z)
        ground_up_continuous = struct.pack("?", True)

        primary_bit_mask = 0
        for i, section in enumerate(self.sections):
            if section.blocks:
                primary_bit_mask |= (1 << i)
        primary_bit_mask = struct.pack(">H", primary_bit_mask)

        chunk_data = BytesIO()
        for section in self.sections:
            if section.blocks:
                block_data = bytearray(8192)
                for (coords, block) in section.blocks.items():
                    x, y, z = coords
                    if not (0 <= x < 16 and 0 <= y < 16 and 0 <= z < 16):
                        continue

                    block_type = block['type']
                    metadata = block.get('metadata', 0)
                    index = (y << 8) | (z << 4) | x
                    packed_block = ((block_type << 4) | metadata) & 0xFF
                    block_data[index] = packed_block

                block_light = bytearray(2048)
                skylight = bytearray(2048)

                chunk_data.write(block_data)
                chunk_data.write(block_light)
                chunk_data.write(skylight)

        biomes = bytearray(256)
        chunk_data.write(biomes)

        compressed_data = zlib.compress(chunk_data.getvalue())
        compressed_data_size = write_varint(len(compressed_data))
        chunk_packet_data = chunk_coords + ground_up_continuous + primary_bit_mask + compressed_data_size + compressed_data

        send_packet(conn, 0x21, chunk_packet_data)
        server_out("INFO", f"Chunk data sent (Client: {conn.getpeername()})")

class ChunkSection:
    def __init__(self, y_level):
        self.y_level = y_level
        self.blocks = {}

    def get_block_at_relative(self, x, y, z):
        return self.blocks.get((x, y, z))

    def set_block_at_relative(self, x, y, z, block_data):
        if 'metadata' not in block_data:
            block_data['metadata'] = 0
        self.blocks[(x, y, z)] = block_data

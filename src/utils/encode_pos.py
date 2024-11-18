import struct

# encodes pos to mc packed long
def encode_position(x, y, z):
    return struct.pack('>q', ((x & 0x3FFFFFF) << 38) | ((y & 0xFFF) << 26) | (z & 0x3FFFFFF))
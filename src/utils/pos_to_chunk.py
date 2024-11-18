def pos_to_chunk_int(x, y, z):
    return (x << 16) | (y << 8) | z

def chunk_int_to_pos(value):
    z = value & 0xFF
    y = (value >> 8) & 0xFF
    x = (value >> 16) & 0xFF
    return x, y, z

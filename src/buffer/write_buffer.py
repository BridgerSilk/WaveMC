def write_varint(value: int) -> bytes:
    result = bytearray()
    while value & 0xFFFFFF80:
        result.append((value & 0x7F) | 0x80)
        value >>= 7
    result.append(value & 0x7F)
    return bytes(result)

def write_string(value: str) -> bytes:
    value_bytes = value.encode('utf-8')
    return write_varint(len(value_bytes)) + value_bytes
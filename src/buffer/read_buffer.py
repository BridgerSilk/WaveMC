def read_varint(sock):
    num = 0
    bytes_read = 0
    while True:
        byte = sock.recv(1)
        if not byte:
            raise ConnectionError("Connection lost while reading VarInt")
        byte = ord(byte)
        num |= (byte & 0x7F) << (7 * bytes_read)
        bytes_read += 1
        if (byte & 0x80) == 0:
            break
        if bytes_read > 5:
            raise ValueError("VarInt is too large")
    return num

def read_string(sock):
    length = read_varint(sock)
    if length > 32767:              
        raise ValueError("String too long")
    data = sock.recv(length)
    if len(data) != length:
        raise ConnectionError("Connection lost while reading String")
    return data.decode('utf-8')
import struct
from buffer.write_buffer import *
from net.server_status import *
from data.server_options import *
from data.pvn_map import *
from enums.state import *
from packets.packetmap import *
from datetime import datetime

def send_status_response(conn):
    motd = DESC
    version = ServerStatusResponse.Version(PVN, pvn_map[PVN])
    players = ServerStatusResponse.Players(ONLINE_PLAYERS, MAX_PLAYERS)

    status_response = ServerStatusResponse(motd, players, version)
    json_response = status_response.to_json()

    response_packet = write_varint(len(json_response)) + json_response.encode('utf-8')
    send_packet(conn, 0x00, response_packet)
    server_out("DEBUG", f"Status response sent: {json_response}") # for some fucking reason if i comment out this line (which is only for debugging) the whole status response breaks. So ig this will have to stay, someone tell me wtf is going on here

def send_packet(sock, packet_id, data=b""):
    packet = write_varint(len(data) + 1) + write_varint(packet_id) + data
    sock.sendall(packet)

def send_handshake(conn, host, port, PVN):
    next_state = State.status.value
    handshake_packet = (
        write_varint(0x00) +
        write_varint(PVN) +
        write_string(host) +
        struct.pack(">H", port) +
        write_varint(next_state)
    )
    send_packet(conn, 0x00, handshake_packet)

CONSOLE_COLORS = {
    "ERROR": '\033[91m',
    "WARNING": '\033[93m',
    "DEBUG": '\033[96m',
    "INFO": '\033[92m',
}

def server_out(type, msg):
    current_time = datetime.now().strftime("%H:%M:%S")
    print(CONSOLE_COLORS[type] + current_time + f" [{type}] " + msg)
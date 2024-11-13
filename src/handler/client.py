import struct
import uuid
from net.io import *
from buffer.read_buffer import *
from buffer.write_buffer import *
from enums.state import State
from enums.gamemode import *
from enums.dimension import *
from enums.difficulty import *
from data.server_options import *
from enums.leveltype import *

def handle_client(conn, addr):

    server_out("INFO", f"Client is connecting... (Client: {addr})")

    try:
        packet_length = read_varint(conn)
        packet_id = read_varint(conn)

        if packet_id != 0x00:
            server_out("ERROR", f"Unexpected packet ID during handshake: {packet_id} (Client: {addr})")
            return

        PVN = read_varint(conn)
        if PVN != PVN:
            server_out("ERROR", f"Unsupported protocol version: {PVN} (Client: {addr})")
            return

        hostname = read_string(conn)
        port = struct.unpack('>H', conn.recv(2))[0]
        next_state = read_varint(conn)

        if next_state == State.status.value:
            server_out("INFO", f"Handling server list ping request... (Client: {addr})")
            send_status_response(conn)
            return

        elif next_state == State.login.value:
            packet_length = read_varint(conn)
            packet_id = read_varint(conn)
            if packet_id != 0x00:
                server_out("ERROR", f"Unexpected packet ID during login (Client: {addr})")
                return

            username = read_string(conn)
            server_out("INFO", f"Received Login Start packet. Username: {username} (Client: {addr})")

            player_uuid = str(uuid.uuid4())
            uuid_data = write_varint(len(player_uuid)) + player_uuid.encode('utf-8')
            username_data = write_varint(len(username)) + username.encode('utf-8')
            send_packet(conn, 0x02, uuid_data + username_data)
            server_out("INFO", f"Login success sent for player '{username}' (Client: {addr})")

            server_out("INFO", f"Forwarding to play state... (Client: {addr})")

            entity_id = 1
            gamemode = Gamemode.survival.value
            dimension = Dimension.overworld.value
            difficulty = Difficulty.easy.value
            max_players = MAX_PLAYERS
            level_type = LevelType.default.value
            reduced_debug_info = False

            join_game_data = (
                struct.pack(">iBbbB", entity_id, gamemode, dimension, difficulty, max_players) +
                write_varint(len(level_type)) + level_type.encode('utf-8') +
                struct.pack("?", reduced_debug_info)
            )
            send_packet(conn, 0x01, join_game_data)
            server_out("INFO", f"Join game packet sent (Client: {addr})")

            while True:
                conn.sendall(write_varint(0x00))
                data = conn.recv(1024)
                if not data:
                    server_out("INFO", f"Client disconnected (Client: {addr})")
                    break

    except (ConnectionError, ValueError) as e:
        server_out("ERROR", f"Error with client {addr}: {e}")
    finally:
        conn.close()
        server_out("INFO", f"Client disconnected (Client: {addr})")
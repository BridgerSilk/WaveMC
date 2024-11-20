from world.world import *
from world.mc_chunk import *
from enums.state import *
from utils.encode_pos import *
from net.io import *
from enums.gamemode import *
from data.server_options import *
from enums.dimension import *
from enums.difficulty import *
from enums.leveltype import *
import struct
import uuid
from packets.packetmap import *
from buffer.read_buffer import *
from buffer.write_buffer import *
# packets
from packets.out.player_pos_and_look import *
from packets.out.held_item_change import *
from packets.out.entity_effect import *
from packets.out.update_health import *

# packets
player_pos_and_look = PlayerPositionAndLook(SPAWN_X, SPAWN_Y, SPAWN_Z, YAW, PITCH, 0x00) # 0x00 -> flag byte

# test packets
held_item_change = HeldItemChange(5) # testing
entity_effect = EntityEffect(1, 0x26, 0x08, 50, False) # fix - doesnt work -> see entity_effect.py
update_health = UpdateHealth(10, 20, 3) # testing

world = World(Dimension.overworld.value, Difficulty.normal.value, LevelType.default.value)

def handle_client(conn, addr):
    try:
        packet_length = read_varint(conn)
        packet_id = read_varint(conn)

        if packet_id != packetmap_server[State.handshake.value]["handshaking"]:
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
            if packet_id != packetmap_client[State.login.value]["disconnect"]:
                server_out("ERROR", f"Unexpected packet ID during login (Client: {addr})")
                return

            username = read_string(conn)
            server_out("INFO", f"Received Login Start packet. Username: {username} (Client: {addr})")

            player_uuid = str(uuid.uuid4())
            uuid_data = write_varint(len(player_uuid)) + player_uuid.encode('utf-8')
            username_data = write_varint(len(username)) + username.encode('utf-8')
            send_packet(conn, packetmap_client[State.login.value]["login_success"], uuid_data + username_data)
            server_out("INFO", f"Login success sent for player '{username}' (Client: {addr})")

            entity_id = 1 # fix - uhm this is supposed to be random
            gamemode = Gamemode.creative.value # todo - change to survival later, creative for testing
            dimension = Dimension.overworld.value
            difficulty = Difficulty.normal.value
            max_players = MAX_PLAYERS
            level_type = LevelType.default.value
            reduced_debug_info = False
            # optimize - when creating multiple worlds these values may not match the values of other worlds and cause problems, therefore change this later

            join_game_data = (
                struct.pack(">iBbbB", entity_id, gamemode, dimension, difficulty, max_players) +
                write_varint(len(level_type)) + level_type.encode('utf-8') +
                struct.pack("?", reduced_debug_info)
            )
            send_packet(conn, 0x01, join_game_data)
            server_out("INFO", f"Join game packet sent (Client: {addr})")

            player_x, player_y, player_z = SPAWN_X, SPAWN_Y, SPAWN_Z
            spawn_position = encode_position(player_x, player_y, player_z)
            send_packet(conn, 0x05, spawn_position)
            server_out("INFO", f"Sent spawn position: ({player_x}, {player_y}, {player_z})")

            for chunk_x in range(-1, 2):
                for chunk_z in range(-1, 2):
                    chunk_manager = world.get_chunk_at(chunk_x * 16, chunk_z * 16)
                    chunk_manager.send_chunk_data(conn)

            # sending this packet closes the downloading terrain screen
            send_packet(conn, player_pos_and_look.id, player_pos_and_look.packet)

            send_packet(conn, held_item_change.id, held_item_change.packet) # testing
            send_packet(conn, update_health.id, update_health.packet) # testing
            send_packet(conn, entity_effect.id, entity_effect.packet) # testing

            while True:
                conn.sendall(write_varint(0x00)) # keep alive
                data = conn.recv(1024)
                if not data:
                    server_out("INFO", f"Client disconnected (Client: {addr})")
                    break

    except (ConnectionError, ValueError) as e:
        server_out("ERROR", f"Error with client {addr}: {e}")
    finally:
        conn.close()
        server_out("INFO", f"Client disconnected (Client: {addr})")


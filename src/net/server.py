import socket
from data.server_options import *
from handler.client import *
from world.world import *
from enums.difficulty import *
from enums.dimension import *
from enums.leveltype import *
from handler.client import *

world = World(Dimension.overworld.value, Difficulty.normal.value, LevelType.default.value)

def start_server():
    server_out("INFO", "Starting Server...")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()

        # world generation
        world.generate_world()

        server_out("INFO", f"Server started on {HOST}:{PORT}")

        while True:
            conn, addr = server_socket.accept()
            handle_client(conn, addr)
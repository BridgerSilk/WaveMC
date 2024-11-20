from world.mc_chunk import *
from data.server_options import *
from net.io import *

class World:
    def __init__(self, dimension, difficulty, level_type):
        self.dimension = dimension
        self.difficulty = difficulty
        self.level_type = level_type
        self.spawn_x = SPAWN_X
        self.spawn_y = SPAWN_Y
        self.spawn_z = SPAWN_Z
        self.chunks = set()

    def get_chunk_at(self, x, z):
        chunk_x = x // 16
        chunk_z = z // 16

        for chunk in self.chunks:
            if chunk.x == chunk_x and chunk.z == chunk_z:
                return chunk

        chunk = Chunk(chunk_x, chunk_z)
        self.chunks.add(chunk)
        return chunk

    def get_block_at(self, x, y, z):
        chunk = self.get_chunk_at(x, z)
        if chunk is None:
            return {'type': 0, 'data': 0}
        return chunk.get_block_at(x, y, z)

    def set_block_at(self, x, y, z, block_data):
        chunk_x = x // 16
        chunk_z = z // 16
        local_x = x % 16
        local_z = z % 16

        chunk = self.get_chunk_at(chunk_x, chunk_z)
        chunk.set_block_at(local_x, y, local_z, block_data)

    def generate_world(self):
        server_out("INFO", f"Initializing world settings: (Dimension: {self.dimension}, Difficulty: {self.difficulty}, LevelType: {self.level_type})")
        server_out("INFO", "Generating world...")
        for x in range(self.spawn_x - 32, self.spawn_x + 32):
            for z in range(self.spawn_z - 32, self.spawn_z + 32):
                self.set_block_at(x, 62, z, {'type': 2, 'metadata': 0})
        server_out("INFO", "Finished generating world.")
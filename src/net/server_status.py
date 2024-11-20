import json

class ServerStatusResponse:
    class Players:
        def __init__(self, online, max):
            self.online = online
            self.max = max
    class Version:
        def __init__(self, protocol, name):
            self.protocol = protocol
            self.name = name
    def __init__(self, description, players, version):
        self.description = description
        self.players = players
        self.version = version
    def to_json(self):
        response_dict = {
            "description": self.description,
            "players": {
                "online": self.players.online,
                "max": self.players.max,
            },
            "version": {
                "name": self.version.name,
                "protocol": self.version.protocol,
            }
        }
        return json.dumps(response_dict)
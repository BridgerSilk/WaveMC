from enums.state import *

packetmap_client = {
    State.status.value: {
        "status_response": 0x00,
        "pong": 0x01,
    },
    State.login.value: {
        "disconnect": 0x00,
        "encryption_request": 0x01,
        "login_success": 0x02,
        "set": 0x02,
    },
    State.play.value: {
        "keep_alive": 0x00,
        "join_game": 0x01,
        "chat_message": 0x02
    },
}
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
        "set_compression": 0x02,
    },
    State.play.value: {
        "keep_alive": 0x00,
        "join_game": 0x01,
        "chat_message": 0x02,
        # todo - 0x03, 0x04
        "spawn_pos": 0x05,
        "update_health": 0x06,
        "player_pos_and_look": 0x08,
        "open_sign_editor": 0x36,
        "disconnect": 0x40,
        "set_slot": 0x2F,
        "close_window": 0x2E,
        # todo - 0x09 and 0x1D are easy to implement
        "held_item_change": 0x09,
        "entity_effect": 0x1D, # fix - entity effect packet doesnt work apparently
    },
}               

packetmap_server = {
    State.handshake.value: {
        "handshaking": 0x00,
    }
}
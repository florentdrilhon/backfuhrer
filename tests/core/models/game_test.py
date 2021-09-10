from core.models.game import *


def test_dict_are_complete():
    for game_type in GameType:
        assert game_type in GAME_TYPE_MAPPING.values()
        assert game_type in GAME_DEFAULT_IMAGES


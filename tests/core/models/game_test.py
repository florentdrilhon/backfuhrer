from tests.core.persist.utils import new_game
from core.persist import games_repository


def test_serialize():
    game = new_game()
    ser_game = game.serialize()
    assert isinstance(ser_game, dict)
    assert ser_game['_id'] == game.uid
    assert ser_game['name'] == game.name
    assert ser_game['description'] == game.description
    assert ser_game['rules'] == game.rules
    assert ser_game['duration_min'] == game.duration_min
    assert ser_game['number_of_players'] == game.number_of_players
    assert ser_game['image'] == game.image
    assert ser_game['game_type'] == game.game_type.value
    assert ser_game['created_at'] == game.created_at
    assert ser_game['updated_at'] == game.updated_at


def test_from_db():
    game = new_game()
    games_repository.create_one(game)



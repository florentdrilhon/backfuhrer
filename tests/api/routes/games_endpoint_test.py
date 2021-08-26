from core.models.game import Game, GameType
from tests.core.persist import utils
from tests.utils import one_of, random_number
from tests.fixtures.app import client


def test_list_games(client):
    new_game = utils.new_game()
    response = client.get('/games')
    assert response.status_code == 200
    games = [Game.from_db(d) for d in response.get_json()]
    assert new_game in games


def test_list_games_by_game_type(client):
    game_type = one_of(GameType)
    new_game = utils.new_game(game_type=game_type)
    response = client.get(f'/games?type={game_type.value}')
    assert response.status_code == 200
    games = [Game.from_db(d) for d in response.get_json()]
    assert new_game in games


def test_list_games_by_min_player(client):
    min_player = random_number(5, 9)
    new_game = utils.new_game(number_of_players=(random_number(1, 4), 10))
    response = client.get(f'/games?min_number_player={min_player}')
    assert response.status_code == 200
    games = [Game.from_db(d) for d in response.get_json()]
    assert new_game in games
    for game in games:
        assert game.number_of_players[1] >= min_player


def test_list_games_by_max_player(client):
    max_player = random_number(5, 9)
    new_game = utils.new_game(number_of_players=(4, random_number(9, 11)))
    response = client.get(f'/games?max_number_player={max_player}')
    assert response.status_code == 200
    games = [Game.from_db(d) for d in response.get_json()]
    assert new_game in games
    for game in games:
        assert game.number_of_players[0] <= max_player

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


def test_list_games_by_number_players(client):
    number_players = random_number(5, 9)
    new_game = utils.new_game(number_of_players=(number_players - 1, number_players + 1))
    response = client.get(f'/games?number_players={number_players}')
    assert response.status_code == 200
    games = [Game.from_db(d) for d in response.get_json()]
    assert new_game in games
    for game in games:
        assert game.number_of_players[1] >= number_players
        assert game.number_of_players[0] <= number_players

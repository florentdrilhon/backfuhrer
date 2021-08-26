from core.models.game import Game, GameType
from core.persist import games_repository
from tests.core.persist import utils
from tests.utils import list_of, one_of, random_number


def test_create_one():
    game = Game()
    result = games_repository.create_one(game)
    assert result.inserted_id == str(game._id)


def test_find_by_id():
    game = utils.new_game()
    db_game = games_repository.find_by(game._id)
    assert db_game == game


def test_list_by_all():
    games = list_of(utils.new_game, min_count=3)
    retrieved_games = games_repository.list_by()
    for game in games:
        assert game in retrieved_games


def test_list_by_game_type():
    my_game_type = one_of(GameType)
    good_games = list_of(lambda: utils.new_game(game_type=my_game_type), min_count=3)
    not_good_games = list_of(lambda: utils.new_game(game_type=one_of(GameType,
                                                                     excluding=[my_game_type])))
    retrieved_games = games_repository.list_by(game_types=[my_game_type])
    for game in good_games:
        assert game in retrieved_games
    for game in not_good_games:
        assert game not in retrieved_games
    for game in retrieved_games:
        assert game.game_type == my_game_type


def test_list_by_min_number_player():
    good_games = list_of(lambda: utils.new_game(number_of_players=(random_number(5, 7), random_number(8, 10))),
                         min_count=3)
    not_good_games = list_of(lambda: utils.new_game(number_of_players=(random_number(1, 2), random_number(3, 4))))
    retrieved_games = games_repository.list_by(min_number_players=5)
    for game in good_games:
        assert game in retrieved_games
    for game in not_good_games:
        assert game not in retrieved_games
    for game in retrieved_games:
        assert game.number_of_players[1] >= 5


def test_list_by_max_number_player():
    good_games = list_of(lambda: utils.new_game(number_of_players=(random_number(1, 3), random_number(4, 6))),
                         min_count=3)
    not_good_games = list_of(lambda: utils.new_game(number_of_players=(random_number(7, 9), random_number(10, 12))))
    retrieved_games = games_repository.list_by(max_number_players=6)
    for game in good_games:
        assert game in retrieved_games
    for game in not_good_games:
        assert game not in retrieved_games
    for game in retrieved_games:
        assert game.number_of_players[0] <= 6


def test_delete_by():
    games = list_of(lambda: utils.new_game())
    result = games_repository.delete_by([g._id for g in games])
    assert result.deleted_count == len(games)


def test_delete_all():
    _ = games_repository.delete_by()
    retrieved_games = games_repository.list_by()
    assert len(retrieved_games) == 0

from core.models.game import Game
from core.persist import games_repository
from tests.core.persist import utils
from tests.utils import list_of


def test_create_one():
    game = Game()
    result = games_repository.create_one(game)
    assert result.inserted_id == str(game._id)


def test_find_by_id():
    game = utils.new_game()
    db_game = games_repository.find_by(game._id)
    assert db_game == game


def test_delete_by():
    games = list_of(lambda: utils.new_game())
    result = games_repository.delete_by([g._id for g in games])
    assert result.deleted_count == len(games)


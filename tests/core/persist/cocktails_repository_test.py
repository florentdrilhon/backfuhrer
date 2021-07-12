from core.models.cocktail import Cocktail
from core.persist import cocktails_repository
from tests.core.persist import utils
from tests.utils import list_of


def test_create_one():
    cocktail = Cocktail()
    result = cocktails_repository.create_one(cocktail)
    assert result.inserted_id == str(cocktail._id)


def test_find_by_id():
    cocktail = utils.new_cocktail()
    db_game = cocktails_repository.find_by(cocktail._id)
    assert db_game == cocktail

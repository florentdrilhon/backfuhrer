from core.models.cocktail import Cocktail, CocktailType
from core.persist import cocktails_repository
from tests.core.persist import utils
from tests.utils import list_of, one_of, random_number


def test_create_one():
    cocktail = Cocktail()
    result = cocktails_repository.create_one(cocktail)
    assert result.inserted_id == str(cocktail._id)


def test_find_by_id():
    cocktail = utils.new_cocktail()
    db_cocktail = cocktails_repository.find_by(cocktail._id)
    assert db_cocktail == cocktail


def test_list_by_all():
    cocktails = list_of(utils.new_cocktail, min_count=3)
    retrieved_cocktails = cocktails_repository.list_by()
    for cocktail in cocktails:
        assert cocktail in retrieved_cocktails


def test_list_by_cocktail_type():
    alcohol_cocktails = list_of(lambda: utils.new_cocktail(cocktail_type=CocktailType.Alcohol), min_count=3)
    non_alcohol_cocktails = list_of(lambda: utils.new_cocktail(cocktail_type=one_of(CocktailType,
                                                                                    excluding=[CocktailType.Alcohol])))
    retrieved_cocktails = cocktails_repository.list_by(types=[CocktailType.Alcohol])
    for cocktail in alcohol_cocktails:
        assert cocktail in retrieved_cocktails
    for cocktail in non_alcohol_cocktails:
        assert cocktail not in retrieved_cocktails


def test_list_by_preparation_time():
    good_cocktails = list_of(lambda: utils.new_cocktail(preparation_time_min=random_number(1, 5)), min_count=3)
    not_good_cocktails = list_of(lambda: utils.new_cocktail(preparation_time_min=random_number(6, 10)))
    retrieved_cocktails = cocktails_repository.list_by(max_preparation_time=5)
    for cocktail in good_cocktails:
        assert cocktail in retrieved_cocktails
    for cocktail in not_good_cocktails:
        assert cocktail not in retrieved_cocktails



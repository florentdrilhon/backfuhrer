from core.models.beer import Beer, BeerType, BeerCategory
from core.persist import beers_repository
from tests.core.persist.utils import new_beer
from tests.core.persist import utils
from tests.utils import list_of, one_of, random_number


def test_create_one():
    beer = Beer()
    result = beers_repository.create_one(beer)
    assert result.inserted_id == str(beer._id)


def test_find_by_id():
    beer = utils.new_beer()
    db_beer = beers_repository.find_by(beer._id)
    assert db_beer == beer


def test_list_by_all():
    beers = list_of(utils.new_beer, min_count=3)
    retrieved_beers = beers_repository.list_by()
    for beer in beers:
        assert beer in retrieved_beers


def test_list_by_beer_type():
    my_beer_type = one_of(BeerType)
    good_beers = list_of(lambda: utils.new_beer(beer_type=my_beer_type), min_count=3)
    not_good_beers = list_of(lambda: utils.new_beer(beer_type=one_of(BeerType,
                                                                     excluding=[my_beer_type])))
    retrieved_beers = beers_repository.list_by(beer_types=[my_beer_type])
    for beer in good_beers:
        assert beer in retrieved_beers
    for beer in not_good_beers:
        assert beer not in retrieved_beers
    for beer in retrieved_beers:
        assert beer.beer_type == my_beer_type


def test_list_by_categories():
    my_beer_category = one_of(BeerCategory)
    good_beers = list_of(lambda: utils.new_beer(category=my_beer_category), min_count=3)
    not_good_beers = list_of(lambda: utils.new_beer(category=one_of(BeerCategory,
                                                                    excluding=[my_beer_category])))
    retrieved_beers = beers_repository.list_by(categories=[my_beer_category])
    for beer in good_beers:
        assert beer in retrieved_beers
    for beer in not_good_beers:
        assert beer not in retrieved_beers
    for beer in retrieved_beers:
        assert beer.category == my_beer_category


def test_list_by_max_price():
    good_beers = list_of(lambda: utils.new_beer(price=random_number(10, 20)),
                         min_count=3)
    not_good_beers = list_of(lambda: utils.new_beer(price=random_number(21, 30)))
    retrieved_beers = beers_repository.list_by(max_price=20)
    for beer in good_beers:
        assert beer in retrieved_beers
    for beer in not_good_beers:
        assert beer not in retrieved_beers
    for beer in retrieved_beers:
        assert beer.price <= 20


def test_delete_by():
    beers = list_of(lambda: utils.new_beer())
    result = beers_repository.delete_by([g._id for g in beers])
    assert result.deleted_count == len(beers)


def test_delete_all():
    _ = beers_repository.delete_by()
    retrieved_beers = beers_repository.list_by()
    assert len(retrieved_beers) == 0


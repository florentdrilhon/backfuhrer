from core.models.beer import Beer, BeerType, BeerCategory
from tests.core.persist import utils
from tests.utils import one_of, random_number, ascii_string, list_of
from tests.fixtures.app import client


def test_list_beers(client):
    new_beer = utils.new_beer()
    response = client.get('/beers')
    assert response.status_code == 200
    beers = [Beer.from_db(d) for d in response.get_json()]
    assert new_beer in beers


def test_list_beers_by_beer_type(client):
    beer_type = one_of(BeerType)
    new_beer = utils.new_beer(beer_type=beer_type)
    response = client.get(f'/beers?type={beer_type.value}')
    assert response.status_code == 200
    beers = [Beer.from_db(d) for d in response.get_json()]
    assert new_beer in beers


def test_list_beers_by_category(client):
    category = one_of(BeerCategory)
    new_beer = utils.new_beer(category=category)
    response = client.get(f'/beers?category={category.value}')
    assert response.status_code == 200
    beers = [Beer.from_db(d) for d in response.get_json()]
    assert new_beer in beers


def test_list_beers_by_max_price(client):
    max_price = random_number(20, 30)
    new_beer = utils.new_beer(price=random_number(1, max_price))
    response = client.get(f'/beers?max_price={max_price}')
    assert response.status_code == 200
    beers = [Beer.from_db(d) for d in response.get_json()]
    assert new_beer in beers
    for beer in beers:
        assert beer.price <= max_price


def test_search_by_name(client):
    name = ascii_string()
    new_beers = list_of(lambda: utils.new_beer(name=name), count=3)
    response = client.get(f'/beers/search?name={name}')
    assert response.status_code == 200
    beers = [Beer.from_db(d) for d in response.get_json()]
    assert len(beers) >= len(new_beers)
    for beer in new_beers:
        assert beer in beers

from core.models.cocktail import Cocktail, CocktailType
from tests.core.persist import utils
from tests.utils import one_of, random_number, ascii_string, list_of
from tests.fixtures.app import client


def test_list_cocktails(client):
    new_cocktail = utils.new_cocktail()
    response = client.get('/cocktails')
    assert response.status_code == 200
    cocktails = [Cocktail.from_db(d) for d in response.get_json()]
    assert new_cocktail in cocktails


def test_list_cocktails_by_cocktail_type(client):
    cocktail_type = one_of(CocktailType)
    new_cocktail = utils.new_cocktail(cocktail_type=cocktail_type)
    response = client.get(f'/cocktails?type={cocktail_type.value}')
    assert response.status_code == 200
    cocktails = [Cocktail.from_db(d) for d in response.get_json()]
    assert new_cocktail in cocktails
    for cocktail in cocktails:
        assert cocktail.cocktail_type == cocktail_type


def test_list_cocktails_max_preparation_time(client):
    max_preparation_time = random_number(20, 30)
    new_cocktail = utils.new_cocktail(preparation_time_min=random_number(5, max_preparation_time))
    response = client.get(f'/cocktails?max_preparation_time={max_preparation_time}')
    assert response.status_code == 200
    cocktails = [Cocktail.from_db(d) for d in response.get_json()]
    assert new_cocktail in cocktails
    for cocktail in cocktails:
        assert cocktail.preparation_time_min <= max_preparation_time


def test_search_by_name(client):
    name = ascii_string()
    new_cocktails = list_of(lambda: utils.new_cocktail(name=name), count=3)
    response = client.get(f'/cocktails/search?name={name}')
    assert response.status_code == 200
    cocktails = [Cocktail.from_db(d) for d in response.get_json()]
    assert len(cocktails) >= len(new_cocktails)
    for cocktail in new_cocktails:
        assert cocktail in cocktails

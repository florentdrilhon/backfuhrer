from core.models.beer import *


def test_dict_are_complete():
    for beer_type in BeerType:
        assert beer_type in BEER_TYPE_MAPPING.values()
    for beer_category in BeerCategory:
        assert beer_category in BEER_CATEGORY_MAPPING.values()
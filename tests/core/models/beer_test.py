from core.models.beer import *


def test_dict_are_complete():
    for beer_type in BeerType:
        assert beer_type in BEER_TYPES_NAMES
        assert beer_type in BEER_TYPE_MAPPING.values()
        assert beer_type in BEER_NAMES_TYPES.values()
    for beer_category in BeerCategory:
        assert beer_category in BEER_CATEGORIES_NAMES
        assert beer_category in BEER_NAMES_CATEGORIES.values()
        assert beer_category in BEER_CATEGORY_MAPPING.values()
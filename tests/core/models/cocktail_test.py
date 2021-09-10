from core.models.cocktail import *


def test_dict_are_complete():
    for cocktail_type in CocktailType:
        assert cocktail_type in COCKTAIL_TYPE_MAPPING.values()

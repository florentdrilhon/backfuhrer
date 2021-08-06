from core.models.cocktail import *


def test_dict_are_complete():
    for cocktail_type in CocktailType:
        assert cocktail_type in COCKTAIL_TYPES_NAMES
        assert cocktail_type in COCKTAIL_TYPE_MAPPING.values()
        assert cocktail_type in COCKTAIL_NAMES_TYPES.values()

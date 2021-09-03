from core.services.search_service import *

from core.models.game import Game
from tests.utils import ascii_string, list_of
from tests.core.persist import utils


def test_name_similarity():
    name = ascii_string()
    good_entities = list_of(lambda: utils.new_game(name=name))
    bad_entities = list_of(lambda: utils.new_game(name=ascii_string(count=50)))
    entities_similarities = name_similarity(name, good_entities + bad_entities)
    for entity in good_entities:
        assert entities_similarities[entity._id] == 1.0
    for entity in bad_entities:
        assert entities_similarities[entity._id] < 0.2


def test_search_by_name():
    name = ascii_string()
    good_entities = list_of(lambda: utils.new_game(name=name))
    searched_entities = search_by_name(name, collection=Collection.Games)
    for e in good_entities:
        assert e in searched_entities

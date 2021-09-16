from typing import List, Optional, Dict

from difflib import SequenceMatcher
from uuid import UUID

import unidecode as unidecode

from core.models.enum import Collection, Entity
from core.persist import games_repository, beers_repository, mamie_nova_advices_repository, cocktails_repository

DEFAULT_REPO_LISTER = {
    Collection.Games: games_repository.list_by,
    Collection.Beers: beers_repository.list_by,
    Collection.Cocktails: cocktails_repository.list_by,
    Collection.MamieNovaAdvices: mamie_nova_advices_repository.list_by
}

"""
The method used here to set up a search function is functional but only because the DB has not much entities
Above a certain number of entities, it can begin to be slow
If the service becomes more and more slow, and the amount of data becoming more important, think of using
the search index included in mongo db atlas service :
- https://www.mongodb.com/atlas/search

I didn't use it because free version includes the use of only 3 indexes, as we have 4 collections needing the index,
I figured out an other solution to do so
"""


def clean_string(string: str) -> str:
    """
    :param string: string to clean
    :return: a string without spaces, punctuation, special characters and accents
    """
    res = string.lower()
    res = res.replace(" ", "")
    res = unidecode.unidecode(res)
    return res


def name_similarity(searched_name: str, entities: List[Entity]) -> Dict[UUID, float]:
    """
    :param searched_name: str provided by the query to compare with entities
    :param entities: entities which name to compare with searched_name

    :return: the Dict of each entity id and its associated similarity with the searched_name
    """
    res = {}
    for entity in entities:
        name = clean_string(entity.name)
        similarity = SequenceMatcher(None, name, clean_string(searched_name)).ratio()
        res[entity._id] = similarity
    return {x: y for x, y in sorted(res.items(), key=lambda t: t[1], reverse=True)}


def search_by_name(searched_name: str,
                   collection: Collection,
                   similarity_threshold: Optional[float] = 0.35) -> List[Entity]:
    """
    :param searched_name: name from the search query to look for into the entities
    :param collection: the collection from which get the similar entities
    :param similarity_threshold: similarity measure above which an entity is considered a minimum similar
                                with searched name, must be between 0 and 1
    :return: list of entities which name is close enough to the compared one
    """
    # gather all entities
    lister = DEFAULT_REPO_LISTER[collection]
    entities = lister()
    entities_ids_mappping = {e._id: e for e in entities}
    # compare the proximity
    entities_similarities = name_similarity(searched_name, entities)
    res = []
    for entity_id, similarity in entities_similarities.items():
        if similarity > similarity_threshold:
            res.append(entities_ids_mappping[entity_id])
    return res

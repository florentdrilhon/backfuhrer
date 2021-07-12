import logging

from typing import Optional, List
from uuid import UUID

from pymongo import MongoClient
from pymongo.results import InsertOneResult

from core.config import config
from core.models.cocktail import Cocktail, CocktailType

logger = logging.getLogger(__name__)

client = MongoClient(config.mongo_client.uri)
db = client.get_database(name=config.mongo_client.db_name)
cocktails = db.get_collection(name="cocktails")


def find_all_types(types: Optional[List[CocktailType]] = None) -> List[Cocktail]:
    conditions = {}
    if types is not None:
        conditions["cocktail_type"] = {'$in': types}
    data = None
    try:
        data = cocktails.find(conditions)
    except TypeError:
        logger.error('Error when getting cocktails from DB: type specified are wrong')
    res = []
    if data is not None:
        for obj in data:
            res.append(Cocktail.from_db(obj))
    return res


def find_by(_id: UUID) -> Optional[Cocktail]:
    conditions = {"_id": str(_id)}
    data = None
    try:
        data = cocktails.find(conditions)
    except TypeError:
        logger.error('Error when getting games from DB: type specified are wrong')
    res = None
    if data is not None:
        try:
            res = Cocktail.from_db(data[0])
        except IndexError:
            logger.warning(f'No game with id: "{_id}" found in db')
    return res


def create_one(cocktail: Cocktail) -> InsertOneResult:
    obj = cocktail.to_dict()
    return cocktails.insert_one(obj)

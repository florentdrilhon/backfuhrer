import logging

from typing import Optional, List
from uuid import UUID

from pymongo import MongoClient
from pymongo.results import InsertOneResult, DeleteResult

from core.config import config
from core.models.cocktail import Cocktail, CocktailType

logger = logging.getLogger(__name__)

client = MongoClient(config.mongo_client.uri)
db = client.get_database(name=config.mongo_client.db_name)
cocktails = db.get_collection(name="cocktails")


def list_by(types: Optional[List[CocktailType]] = None,
            max_preparation_time: Optional[int] = None) -> List[Cocktail]:
    conditions = {}
    if types is not None and len(types) > 0:
        conditions["cocktail_type"] = {'$in': [t.value for t in types]}
    if max_preparation_time is not None:
        conditions["preparation_time_min"] = {'$lte': max_preparation_time}
    data = None
    try:
        logger.warning(f'Getting cocktail with conditions: {conditions}')
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


def delete_by(ids: Optional[List[UUID]] = None) -> Optional[DeleteResult]:
    conditions = {}
    if ids is not None and len(ids) > 0:
        conditions["_id"] = {'$in': [str(_id) for _id in ids]}
    data = None
    try:
        data = cocktails.delete_many(conditions)
    except TypeError:
        logger.error('Error when deleting games from DB: type specified are wrong')
    return data

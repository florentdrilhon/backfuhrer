import logging

from typing import Optional, List
from uuid import UUID

from pymongo import MongoClient
from pymongo.results import InsertOneResult, DeleteResult

from core.config import config
from core.models.beer import BeerType, BeerCategory, Beer

logger = logging.getLogger(__name__)

client = MongoClient(config.mongo_client.uri)
db = client.get_database(name=config.mongo_client.db_name)
beers = db.get_collection(name="beers")


def list_by(beer_types: Optional[List[BeerType]] = None,
            categories: Optional[List[BeerCategory]] = None,
            max_price: Optional[float] = None) -> List[Beer]:
    conditions = {}
    if beer_types is not None and len(beer_types) > 0:
        conditions["beer_type"] = {'$in': [t.value for t in beer_types]}
    if categories is not None and len(categories) > 0:
        conditions["category"] = {'$in': [c.value for c in categories]}
    if max_price is not None:
        conditions["price"] = {'$lte': max_price}
    data = None
    try:
        data = beers.find(conditions)
    except TypeError:
        logger.error('Error when getting beers from DB: : type specified are wrong')
    res = []
    if data is not None:
        for obj in data:
            res.append(Beer.from_db(obj))
    return res


def find_by(_id: UUID) -> Optional[Beer]:
    conditions = {"_id": str(_id)}
    data = None
    try:
        data = beers.find(conditions)
    except TypeError:
        logger.error('Error when getting beers from DB: type specified are wrong')
    res = None
    if data is not None:
        try:
            res = Beer.from_db(data[0])
        except IndexError:
            logger.warning(f'No beer with id: "{_id}" found in db')
    return res


def create_one(beer: Beer) -> InsertOneResult:
    obj = beer.to_dict()
    return beers.insert_one(obj)


def delete_by(ids: Optional[List[UUID]] = None) -> Optional[DeleteResult]:
    conditions = {}
    if ids is not None and len(ids) > 0:
        conditions["_id"] = {'$in': [str(_id) for _id in ids]}
    data = None
    try:
        data = beers.delete_many(conditions)
    except TypeError:
        logger.error('Error when deleting beers from DB: type specified are wrong')
    return data

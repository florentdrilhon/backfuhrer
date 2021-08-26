import logging

from typing import Optional, List
from uuid import UUID

from pymongo import MongoClient
from pymongo.results import InsertOneResult, DeleteResult

from core.config import config
from core.models.mamie_nova_advice import MamieNovaAdviceType, MamieNovaAdvice

logger = logging.getLogger(__name__)

client = MongoClient(config.mongo_client.uri)
db = client.get_database(name=config.mongo_client.db_name)
mamie_nova_advices = db.get_collection(name="mamie_nova_advices")


def list_by(mamie_nova_advice_types: Optional[List[MamieNovaAdviceType]] = None) -> List[MamieNovaAdvice]:
    conditions = {}
    if mamie_nova_advice_types is not None and len(mamie_nova_advice_types) > 0:
        conditions["mamie_nova_advice_type"] = {'$in': [t.value for t in mamie_nova_advice_types]}
    data = None
    try:
        logger.warning(f'Looking for mamie nova advice with conditions {conditions}')
        data = mamie_nova_advices.find(conditions)
    except TypeError:
        logger.error('Error when getting mamie nova pieces of advice from DB: : type specified are wrong')
    res = []
    if data is not None:
        for obj in data:
            res.append(MamieNovaAdvice.from_db(obj))
    return res


def find_by(_id: UUID) -> Optional[MamieNovaAdvice]:
    conditions = {"_id": str(_id)}
    data = None
    try:
        data = mamie_nova_advices.find(conditions)
    except TypeError:
        logger.error('Error when getting mamie nova advice from DB: type of id specified is wrong')
    res = None
    if data is not None:
        try:
            res = MamieNovaAdvice.from_db(data[0])
        except IndexError:
            logger.warning(f'No mamie_nova_advice with id: "{_id}" found in db')
    return res


def create_one(mamie_nova_advice: MamieNovaAdvice) -> InsertOneResult:
    obj = mamie_nova_advice.to_dict()
    return mamie_nova_advices.insert_one(obj)


def delete_by(ids: Optional[List[UUID]] = None) -> Optional[DeleteResult]:
    conditions = {}
    if ids is not None and len(ids) > 0:
        conditions["_id"] = {'$in': [str(_id) for _id in ids]}
    data = None
    try:
        data = mamie_nova_advices.delete_many(conditions)
    except TypeError:
        logger.error('Error when deleting mamie_nova_advices from DB: type specified are wrong')
    return data

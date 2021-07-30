import logging

from typing import Optional, List
from uuid import UUID

from pymongo import MongoClient
from pymongo.results import InsertOneResult, DeleteResult

from core.config import config
from core.models.game import GameType, Game

logger = logging.getLogger(__name__)

client = MongoClient(config.mongo_client.uri)
db = client.get_database(name=config.mongo_client.db_name)
games = db.get_collection(name="games")


def find_all_types(types: Optional[List[GameType]] = None) -> List[Game]:
    conditions = {}
    if types is not None and len(types) > 0:
        conditions["game_type"] = {'$in': [t.value for t in types]}
    data = None
    try:
        data = games.find(conditions)
    except TypeError:
        logger.error('Error when getting games from DB: : type specified are wrong')
    res = []
    if data is not None:
        for obj in data:
            res.append(Game.from_db(obj))
    return res


def find_by(_id: UUID) -> Optional[Game]:
    conditions = {"_id": str(_id)}
    data = None
    try:
        data = games.find(conditions)
    except TypeError:
        logger.error('Error when getting games from DB: type specified are wrong')
    res = None
    if data is not None:
        try:
            res = Game.from_db(data[0])
        except IndexError:
            logger.warning(f'No game with id: "{_id}" found in db')
    return res


def create_one(game: Game) -> InsertOneResult:
    obj = game.to_dict()
    return games.insert_one(obj)


def delete_by(ids: List[UUID]) -> Optional[DeleteResult]:
    conditions = {"_id": {'$in': [str(_id) for _id in ids]}}
    data = None
    try:
        data = games.delete_many(conditions)
    except TypeError:
        logger.error('Error when deleting games from DB: type specified are wrong')
    return data

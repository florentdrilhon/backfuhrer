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


def list_by(game_types: Optional[List[GameType]] = None,
            number_players: Optional[int] = None) -> List[Game]:
    conditions = {}
    if game_types is not None and len(game_types) > 0:
        conditions["game_type"] = {'$in': [t.value for t in game_types]}
    if number_players is not None:
        conditions["number_of_players.1"] = {'$gte': number_players}
        conditions["number_of_players.0"] = {'$lte': number_players}

    data = None
    try:
        logger.warning(f'Looking for cocktail with conditions {conditions}')
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


def delete_by(ids: Optional[List[UUID]] = None) -> Optional[DeleteResult]:
    conditions = {}
    if ids is not None and len(ids) > 0:
        conditions["_id"] = {'$in': [str(_id) for _id in ids]}
    data = None
    try:
        data = games.delete_many(conditions)
    except TypeError:
        logger.error('Error when deleting games from DB: type specified are wrong')
    return data

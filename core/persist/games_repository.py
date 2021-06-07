import logging

from typing import Optional, List

from pymongo import MongoClient
from pymongo.results import InsertOneResult

from core.config import config
from core.models.game import GameType, Game

logger = logging.getLogger(__name__)


client = MongoClient(config.mongo_client.uri)
db = client.get_database(name=config.mongo_client.db_name)
games = db.get_collection(name="games")


def find_all_types(types: Optional[List[GameType]] = None) -> List[Game]:
    conditions = {}
    if types is not None:
        conditions["game_type"] = {'$in': types}
    data = None
    try:
        data = games.find(conditions)
    except:
        logger.error('Error when getting games from DB')
    res = []
    if data is not None:
        for obj in data:
            res.append(Game.from_db(obj))
    return res


def create_one(game: Game) -> InsertOneResult:
    obj = game.serialize()
    return games.insert_one(obj)

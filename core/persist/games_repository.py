import logging

from typing import Optional, List

from pymongo import MongoClient
from pymongo.database import Collection
from pymongo.results import InsertOneResult

from core.config import config
from core.models.game import GameType, Game

logger = logging.getLogger(__name__)

MONGODB_URI = "mongodb+srv://partyfuhrer:partyfuhrer@cluster0.tt2ct.mongodb.net/partyfuhrer?retryWrites=true&w=majority"
MONGODB_DB_NAME = "partyfuhrer"

client = MongoClient(config.mongo_client.uri)
db = client.get_database(name=config.mongo_client.db_name)
games = db.get_collection(name="games")


def find_all_types( types: Optional[List[GameType]] = None) -> List[Game]:
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


def create_one( game: Game) -> InsertOneResult:
    obj = game.serialize()
    return games.insert_one(obj)


if __name__ == '__main__':
    my_game = Game()
    my_game.name = "test"
    my_game.description = "test"
    my_game.rules = "test"
    my_game.duration_min = 12
    my_game.number_of_players = (12, 25)
    my_game.image = "test"
    my_game.game_type = GameType.Cards
    test = create_one(my_game)
    print(test)

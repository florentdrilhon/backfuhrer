from datetime import datetime
from uuid import uuid1, UUID
from typing import Optional, Tuple
from enum import Enum


class GameType(Enum):
    Cards = 'cards'
    Dice = 'dice'
    MobileApplication = 'mobile_application'
    Other = 'other'


_GAME_TYPES = {cocktailtype.value: cocktailtype for cocktailtype in GameType}


class Game:
    uid: UUID = uuid1()
    name: str
    description: str
    rules: str
    duration_min: int
    number_of_players: Tuple[int, int]
    image: str
    game_type: GameType = GameType.Other
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    # put object in a dict format to insert it in DB

    def serialize(self):
        return {
            '_id': self.uid,
            'name': self.name,
            'description': self.description,
            'rules': self.rules,
            'duration_min': self.duration_min,
            'number_of_players': self.number_of_players,
            'image': self.image,
            'game_type': self.game_type.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def from_db(db_object: dict):
        game = Game()
        game._id = db_object['_id']
        game.name = db_object['name']
        game.description = db_object['description']
        game.rules = db_object['rules']
        game.duration_min = db_object['duration_min']
        game.number_of_players = db_object['number_of_players']
        game.image = db_object['image']
        game.game_type = _GAME_TYPES[db_object['game_type']]
        game.created_at = db_object['created_at']
        game.updated_at = db_object['updated_at']
        return game

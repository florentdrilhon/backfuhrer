from datetime import datetime
from uuid import uuid4, UUID
from typing import Tuple, Optional
from enum import Enum
from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin
from dateutil.tz import tzutc


class GameType(Enum):
    Cards = 'cards'
    Dice = 'dice'
    MobileApplication = 'mobile_application'
    Other = 'other'


@dataclass
class Game(JsonSchemaMixin):
    _id: UUID
    name: Optional[str]
    description: Optional[str]
    rules: Optional[str]
    duration_min: Optional[int]
    number_of_players: Optional[Tuple[int, int]]
    image: Optional[str]
    game_type: Optional[GameType]
    created_at: datetime
    updated_at: datetime

    def __init__(self,
                 _id: Optional[UUID] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 rules: Optional[str] = None,
                 duration_min: Optional[int] = None,
                 number_of_players: Optional[Tuple[int, int]] = None,
                 image: Optional[str] = None,
                 game_type: Optional[GameType] = None,
                 created_at: datetime = datetime.now(tz=tzutc()),
                 updated_at: datetime = datetime.now(tz=tzutc())
                 ):
        self._id = _id or uuid4()
        self.name = name
        self.description = description
        self.rules = rules
        self.duration_min = duration_min
        self.number_of_players = number_of_players
        self.image = image
        self.game_type = game_type
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_db(db_object: dict):
        # put object in a dict format to insert it in DB
        return Game.from_dict(db_object)

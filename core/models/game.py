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


GAME_TYPES_NAMES = {
    GameType.Cards: 'Cartes',
    GameType.Dice: 'Dés',
    GameType.MobileApplication: 'Application mobile',
    GameType.Other: 'Autre'
}

GAME_NAMES_TYPES = {
    name: game_type for game_type, name in GAME_TYPES_NAMES.items()
}

GAME_TYPE_MAPPING = {
    g.value: g for g in GameType
}

GAME_DEFAULT_IMAGES = {
    GameType.Cards: "https://www.letribunaldunet.fr/wp-content/uploads/2018/06/alcool.jpg",
    GameType.Dice: "https://static1.magazine.ribambel.com/articles/1/20/71/@/29680-lancez-les-des-et-observez-le-resultat-v2_article_medium-1.jpg",
    GameType.MobileApplication: "https://static1.magazine.ribambel.com/articles/1/20/71/@/29680-lancez-les-des-et-observez-le-resultat-v2_article_medium-1.jpg",
    GameType.Other : "https://www.jeux-alcool.com/wp-content/uploads/2017/03/beerPong.jpeg"
}


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
        self.name = name or ""
        self.description = description or ""
        self.rules = rules or ""
        self.duration_min = duration_min or 0
        self.number_of_players = number_of_players or (0, 10)
        self.game_type = game_type or GameType.Other
        self.image = image or GAME_DEFAULT_IMAGES[self.game_type]
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_db(db_object: dict):
        """
        take an object from Mongo DB a arg and return a Game object
        """
        return Game.from_dict(db_object)

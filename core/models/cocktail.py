from datetime import datetime
from uuid import uuid4, UUID
from typing import Dict, Optional
from enum import Enum
from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin
from dateutil.tz import tzutc


class CocktailType(Enum):
    Alcohol = 'alcohol'
    Soft = 'soft'
    Other = 'other'


@dataclass
class Cocktail(JsonSchemaMixin):
    _id: UUID
    name: str
    description: str
    ingredients: Dict[str, str]  # name / quantity as a str for now
    preparation_time_min: int
    image: str
    cocktail_type: CocktailType
    created_at: datetime
    updated_at: datetime

    def __init__(self,
                 _id: Optional[UUID] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 ingredients: Optional[Dict[str, str]] = None,
                 preparation_time_min: Optional[int] = None,
                 image: Optional[str] = None,
                 cocktail_type: Optional[CocktailType] = None,
                 created_at: datetime = datetime.now(tz=tzutc()),
                 updated_at: datetime = datetime.now(tz=tzutc())
                 ):
        self._id = _id or uuid4()
        self.name = name
        self.description = description
        self.ingredients = ingredients
        self.preparation_time_min = preparation_time_min
        self.image = image
        self.cocktail_type = cocktail_type
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_db(db_object: dict):
        """
        take an object from Mongo DB a arg and return a Cocktail object
        """
        return Cocktail.from_dict(db_object)

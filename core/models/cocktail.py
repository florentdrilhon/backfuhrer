from datetime import datetime
from uuid import uuid4, UUID
from typing import Dict, Optional, List
from enum import Enum
from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin
from dateutil.tz import tzutc


class CocktailType(Enum):
    Alcohol = 'Alcoolisé'
    Soft = 'Mocktail'
    Other = 'Autre'


COCKTAIL_TYPE_MAPPING = {
    c.value: c for c in CocktailType
}

COCKTAIL_DEFAULT_IMAGE = "https://images.unsplash.com/photo-1536935338788-846bb9981813?ixid=MnwxMjA3fDB8MHxzZWFyY2h8Mnx8Y29ja3RhaWx8ZW58MHx8MHx8&ixlib=rb-1.2.1&w=1000&q=80"


@dataclass
class Cocktail(JsonSchemaMixin):
    _id: UUID
    name: str
    description: str
    recipe: List[str]
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
                 recipe: Optional[List[str]] = None,
                 ingredients: Optional[Dict[str, str]] = None,
                 preparation_time_min: Optional[int] = None,
                 image: Optional[str] = None,
                 cocktail_type: Optional[CocktailType] = None,
                 created_at: datetime = datetime.now(tz=tzutc()),
                 updated_at: datetime = datetime.now(tz=tzutc())
                 ):
        self._id = _id or uuid4()
        self.name = name or ""
        self.description = description or ""
        self.recipe = recipe or [""]
        self.ingredients = ingredients or {"": ""}
        self.preparation_time_min = preparation_time_min or 5
        self.image = image or COCKTAIL_DEFAULT_IMAGE
        self.cocktail_type = cocktail_type or CocktailType.Other
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_db(db_object: dict):
        """
        take an object from Mongo DB a arg and return a Cocktail object
        """
        return Cocktail.from_dict(db_object)

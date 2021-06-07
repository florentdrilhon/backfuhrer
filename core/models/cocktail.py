from datetime import datetime
from uuid import uuid1, UUID
from typing import Optional, Tuple, List, Dict, Any
from enum import Enum


class CocktailType(Enum):
    Alcohol = 'alcohol'
    Soft = 'soft'
    Other = 'other'


_COCKTAIL_TYPES = {cocktailtype.value: cocktailtype for cocktailtype in CocktailType}


class Cocktail:
    uid: UUID = uuid1()
    name: str
    description: str
    # TODO ingredients as enum if needed
    ingredients: Dict[str, str]  # name / quantity as a str for now
    preparation_time_min: int
    image: str
    cocktail_type: CocktailType = CocktailType.Other
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    # put object in a dict format to insert it in DB
    def serialize(self) -> Dict[str, Any]:
        return {
            '_id': self.uid,
            'name': self.name,
            'description': self.description,
            'ingredients': self.ingredients,
            'preparation_time_min': self.preparation_time_min,
            'image': self.image,
            'cocktail_type': self.cocktail_type.value,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    @staticmethod
    def from_db(db_object: dict):
        """
        take an object from Mongo DB a arg and return a Cocktail object
        """
        cocktail = Cocktail()
        cocktail._id = db_object['_id']
        cocktail.name = db_object['name']
        cocktail.description = db_object['description']
        cocktail.ingredients = db_object['ingredients']
        cocktail.preparation_time_min = db_object['preparation_time_min']
        cocktail.image = db_object['image']
        cocktail.cocktail_type = _COCKTAIL_TYPES[db_object['cocktail_type']]
        cocktail.created_at = db_object['created_at']
        cocktail.updated_at = db_object['updated_at']
        return cocktail

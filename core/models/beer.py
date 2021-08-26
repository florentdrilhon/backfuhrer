from datetime import datetime
from uuid import uuid4, UUID
from typing import Tuple, Optional
from enum import Enum
from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin
from dateutil.tz import tzutc


class BeerType(Enum):
    Blond = 'blond'
    Dark = 'dark'
    White = 'white'
    Triple = 'Triple'
    Fruity = 'fruity'


# to get the real name to display for each type
BEER_TYPES_NAMES = {
    BeerType.Blond: "Blonde",
    BeerType.Dark: "Brune",
    BeerType.White: "Blanche",
    BeerType.Triple: "Triple",
    BeerType.Fruity: "Fruitée"
}

# to map a name with its value
BEER_NAMES_TYPES = {
    name: beer_type for beer_type, name in BEER_TYPES_NAMES.items()
}

# to map a type value with its type entity
BEER_TYPE_MAPPING = {
    b.value: b for b in BeerType
}


class BeerCategory(Enum):
    Classical = "classical"
    Cheap = "cheap"
    Strong = "strong"
    Unusual = "unusual"
    Light = 'light'
    Other = 'other'


# each category with its real name to display (admin interface)
BEER_CATEGORIES_NAMES = {
    BeerCategory.Classical: "Les classiques",
    BeerCategory.Cheap: "Les pas chères",
    BeerCategory.Strong: "Les fortes",
    BeerCategory.Unusual: "Les insolites",
    BeerCategory.Light: "Les légères",
    BeerCategory.Other: "Autre"
}

# map the real name of a category with its enum entity
BEER_NAMES_CATEGORIES = {
    name: beer_category for beer_category, name in BEER_CATEGORIES_NAMES.items()
}

# to map a category value with its enum entity
BEER_CATEGORY_MAPPING = {
    beer_category.value: beer_category for beer_category in BeerCategory
}

DEFAULT_IMAGE = "https://static.actu.fr/uploads/2021/08/beer-2218900-1920.jpg"


@dataclass
class Beer(JsonSchemaMixin):
    _id: UUID
    name: Optional[str]
    description: Optional[str]
    price: Optional[float]
    alcohol_percentage: Optional[float]
    image: Optional[str]
    beer_type: Optional[BeerType]
    category: Optional[BeerCategory]
    created_at: datetime
    updated_at: datetime

    def __init__(self,
                 _id: Optional[UUID] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 price: Optional[float] = None,
                 alcohol_percentage: Optional[float] = None,
                 image: Optional[str] = None,
                 beer_type: Optional[BeerType] = None,
                 category: Optional[BeerCategory] = None,
                 created_at: datetime = datetime.now(tz=tzutc()),
                 updated_at: datetime = datetime.now(tz=tzutc())
                 ):
        self._id = _id or uuid4()
        self.name = name or ""
        self.description = description or ""
        self.price = price or 0.0
        self.alcohol_percentage = alcohol_percentage or 0.0
        self.beer_type = beer_type or BeerType.Blond
        self.category = category or BeerCategory.Other
        self.image = image or DEFAULT_IMAGE
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_db(db_object: dict):
        """
        take an object from Mongo DB a arg and return a Beer object
        """
        return Beer.from_dict(db_object)

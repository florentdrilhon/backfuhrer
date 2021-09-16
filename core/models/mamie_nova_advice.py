from datetime import datetime
from uuid import uuid4, UUID
from typing import Optional, Dict
from enum import Enum
from dataclasses import dataclass
from dataclasses_jsonschema import JsonSchemaMixin
from dateutil.tz import tzutc


class MamieNovaAdviceType(Enum):
    Application = 'Application mobile'
    Location = 'Lieux'  # ( endroit)
    Transport = 'Transports'
    Security = 'Sécurité'
    Other = 'Autre'


MAMIE_NOVA_ADVICE_TYPE_MAPPING = {
    g.value: g for g in MamieNovaAdviceType
}

DEFAULT_IMAGE = "https://www.ladn.eu/wp-content/uploads/2019/01/Mamie-sur-Instagram.jpg"


@dataclass
class MamieNovaAdvice(JsonSchemaMixin):
    _id: UUID
    name: Optional[str]
    description: Optional[str]
    detailed_description: Optional[str]
    image: Optional[str]
    mamie_nova_advice_type: Optional[MamieNovaAdviceType]
    links: Optional[Dict[str, str]]
    created_at: datetime
    updated_at: datetime

    def __init__(self,
                 _id: Optional[UUID] = None,
                 name: Optional[str] = None,
                 description: Optional[str] = None,
                 detailed_description: Optional[str] = None,
                 image: Optional[str] = None,
                 mamie_nova_advice_type: Optional[MamieNovaAdviceType] = None,
                 links: Optional[Dict[str, str]] = None,
                 created_at: datetime = datetime.now(tz=tzutc()),
                 updated_at: datetime = datetime.now(tz=tzutc())
                 ):
        self._id = _id or uuid4()
        self.name = name or ""
        self.description = description or ""
        self.detailed_description = detailed_description or ""
        self.mamie_nova_advice_type = mamie_nova_advice_type or MamieNovaAdviceType.Other
        self.image = image or DEFAULT_IMAGE  # TODO
        self.links = links or {" ": " "}
        self.created_at = created_at
        self.updated_at = updated_at

    @staticmethod
    def from_db(db_object: dict):
        """
        take an object from Mongo DB a arg and return a Game object
        """
        return MamieNovaAdvice.from_dict(db_object)

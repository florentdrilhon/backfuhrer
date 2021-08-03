import json
import os
import pyhocon
from pyhocon.converter import HOCONConverter
from dataclasses import dataclass
from dataclasses_json import dataclass_json, Undefined


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class MongoClientConfig:
    uri: str
    db_name: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class FlaskAdminConfig:
    secret_key: str
    auth_username: str
    auth_password: str


@dataclass_json(undefined=Undefined.EXCLUDE)
@dataclass(frozen=True)
class Config:
    mongo_client: MongoClientConfig
    flask_admin: FlaskAdminConfig


def load_conf():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, '..', 'resources/application.conf')
    hocon_config = pyhocon.ConfigFactory.parse_file(file_path)
    json_conf = json.loads(HOCONConverter.to_json(hocon_config, compact=True))
    return Config.schema().load(json_conf)


config: Config = load_conf()

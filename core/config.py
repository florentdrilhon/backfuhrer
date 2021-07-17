import json
import os
from typing import Optional


class MongoClientConfig:
    def __init__(self, uri: str, db_name: str):
        self.uri = uri
        self.db_name = db_name


class FlaskAdminConfig:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key


class Config:

    def __init__(self, mongo_client: Optional[MongoClientConfig], flask_admin: Optional[FlaskAdminConfig]):
        self.mongo_client = mongo_client
        self.flask_admin = flask_admin


def load_conf():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(curr_dir, '..', 'resources/config.json')
    with open(file_path) as json_file:
        data = json.load(json_file)
    client = MongoClientConfig(uri=data["mongo_client"]["uri"],
                               db_name=data["mongo_client"]["db_name"])
    flask = FlaskAdminConfig(secret_key=data["flask-admin"]["secret-key"])
    conf = Config(client, flask)
    return conf


config: Config = load_conf()

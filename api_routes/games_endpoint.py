import logging

from flask import Blueprint, abort, jsonify
from core.persist import games_repository

logger = logging.getLogger(__name__)

games_blueprint = Blueprint('games', __name__)


@games_blueprint.route('', methods=['GET'])
def get_all_games():
    games = games_repository.find_all_types()
    response=[]
    for game in games:
        game_obj = game.serialize()
        response.append(game_obj)
    return jsonify(response)

import logging

from flask import Blueprint, jsonify, request

from core.models.game import Game, GameType, GAME_TYPE_MAPPING
from core.persist import games_repository

logger = logging.getLogger(__name__)

games_blueprint = Blueprint('games', __name__)


@games_blueprint.route('', methods=['GET'])
def get_all_games():
    games = games_repository.find_all_types()
    response = []
    for game in games:
        game_obj = game.to_dict()
        response.append(game_obj)
    return jsonify(response)


@games_blueprint.route('', methods=['POST'])
def create_game():
    games_details = request.json
    try:
        game = Game(
                    name=games_details["name"],
                    description=games_details["description"],
                    rules=games_details["rules"],
                    duration_min=games_details["duration_min"],
                    number_of_players=games_details["number_of_players"],
                    image=games_details["image"],
                    game_type=GAME_TYPE_MAPPING[games_details["game_type"]],
                    )
        res = games_repository.create_one(game)
        if str(res.inserted_id) == str(game._id):
            resp = jsonify('Game added successfully')
            resp.status_code = 200
        else:
            resp = jsonify('Issue when inserting game in DB')
            resp.status_code = 500
    except (KeyError, ValueError):
        logger.warning(f'error when making game from dict : {games_details}')
        resp = jsonify('Issue encountered when inserting game')
        resp.status_code = 500

    return resp

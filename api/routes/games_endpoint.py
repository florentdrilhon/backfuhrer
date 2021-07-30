import logging

from flask import Blueprint, jsonify, request

from core.models.game import Game, GAME_TYPE_MAPPING, GameType
from core.persist import games_repository
from api.admin_interface.auth import auth_required

logger = logging.getLogger(__name__)

games_blueprint = Blueprint('games', __name__)


# TODO add some args here to complete api endpoint
@games_blueprint.route('', methods=['GET'])
def get_all_games():
    games = games_repository.find_all_types()
    response = []
    for game in games:
        game_obj = game.to_dict()
        response.append(game_obj)
    return jsonify(response)


@games_blueprint.route('', methods=['POST'])
@auth_required
def create_game():
    games_details = request.json
    try:
        game = Game(
            name=games_details.get("name"),
            description=games_details.get("description"),
            rules=games_details.get("rules"),
            duration_min=games_details.get("duration_min"),
            number_of_players=games_details.get("number_of_players"),
            image=games_details.get("image"),
            game_type=GAME_TYPE_MAPPING[games_details.get("game_type", GameType.Other)],
        )
        logger.info(f'Inserting game {game.name} in DB')
        res = games_repository.create_one(game)
        if str(res.inserted_id) == str(game._id):
            message = 'Game added successfully'
            logger.info(message)
            status_code = 200
        else:
            message = 'Issue when inserting game in DB'
            logger.warning(message)
            status_code = 500
    except (KeyError, ValueError) as err:
        logger.warning(f'error when making game from dict : {games_details} \n'
                       f'error : {err}')
        message = 'Issue encountered when inserting game'
        status_code = 500

    resp = jsonify(message)
    resp.status_code = status_code
    return resp

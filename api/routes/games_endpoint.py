import logging

from flask import Blueprint, jsonify

from core.models.game import Game, GameType
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


@games_blueprint.route('/insert_test', methods=['GET'])
def test():
    my_game = Game()
    my_game.name = "test"
    my_game.description = "test"
    my_game.rules = "test"
    my_game.duration_min = 12
    my_game.number_of_players = (12, 25)
    my_game.image = "test"
    my_game.game_type = GameType.Cards
    insertion_status = games_repository.create_one(my_game)
    if insertion_status.inserted_id is not None:
        res = {'successfully inserted game ': insertion_status.inserted_id}
    else:
        res = {'error when inserting game': my_game.uid}
    logger.info(f'Insert status : {insertion_status}')
    return jsonify(res)

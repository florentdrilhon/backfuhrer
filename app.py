import logging

from flask import Flask
from flask import request, jsonify

from core.persist import games_repository
from core.models.game import Game, GameType

from api_routes.games_endpoint import games_blueprint

logger = logging.getLogger(__name__)

app = Flask(__name__)


def register_routes(app: Flask = app):
    app.register_blueprint(games_blueprint, url_prefix='/games')


@app.route('/games/insert_test', methods=['GET'])
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
    logger.info(f'Insert status : {test}')
    return jsonify(res)


@app.route('/', methods=['GET'])
def hello():
    res = {'status': "C'est ok mon Daniel"}
    return jsonify(res)


register_routes(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

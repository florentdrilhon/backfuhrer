import logging

from flask import Blueprint, jsonify

from core.models.cocktail import Cocktail, CocktailType
from core.persist import cocktails_repository

logger = logging.getLogger(__name__)

cocktails_blueprint = Blueprint('cocktails', __name__)


@cocktails_blueprint.route('', methods=['GET'])
def get_all_cocktails():
    cocktails = cocktails_repository.find_all_types()
    response = []
    for cocktail in cocktails:
        game_obj = cocktail.serialize()
        response.append(game_obj)
    return jsonify(response)


@cocktails_blueprint.route('/insert_test', methods=['GET'])
def test_cocktail():
    cocktail = Cocktail()
    cocktail.name = "test"
    cocktail.description = "test"
    cocktail.ingredients = {"vodka": "2 cl", "jus d'orange": '20 cl'}
    cocktail.preparation_time_min = 12
    cocktail.image = "test2"
    cocktail.cocktail_type = CocktailType.Alcohol
    insertion_status = cocktails_repository.create_one(cocktail)
    if insertion_status.inserted_id is not None:
        res = {'successfully inserted cocktail ': insertion_status.inserted_id}
    else:
        res = {'error when inserting cocktail': cocktail._id}
    logger.info(f'Insert status : {insertion_status}')
    return jsonify(res)

import logging

from flask import Blueprint, jsonify, request

from core.models.cocktail import Cocktail, COCKTAIL_TYPE_MAPPING, CocktailType
from core.persist import cocktails_repository
from api.admin_interface.auth import auth_required

logger = logging.getLogger(__name__)

cocktails_blueprint = Blueprint('cocktails', __name__)


@cocktails_blueprint.route('', methods=['GET'])
def get_all_cocktails():
    cocktail_types = [COCKTAIL_TYPE_MAPPING.get(g_t, None) for g_t in request.args.getlist('cocktail_type')]
    cocktails = cocktails_repository.list_by(types=cocktail_types)
    response = []
    for cocktail in cocktails:
        cocktail_obj = cocktail.to_dict()
        response.append(cocktail_obj)
    return jsonify(response)


@cocktails_blueprint.route('', methods=['POST'])
@auth_required
def create_cocktail():
    cocktails_details = request.json
    try:
        cocktail = Cocktail(
            name=cocktails_details.get("name"),
            description=cocktails_details.get("description"),
            ingredients=cocktails_details.get("ingredients"),
            preparation_time_min=cocktails_details.get("preparation_time_min"),
            image=cocktails_details.get("image"),
            cocktail_type=COCKTAIL_TYPE_MAPPING[cocktails_details.get("cocktail_type", CocktailType.Other)],
        )
        logger.info(f'Inserting cocktail {cocktail.name} in DB')
        res = cocktails_repository.create_one(cocktail)
        if str(res.inserted_id) == str(cocktail._id):
            message = 'Cocktail added successfully'
            logger.info(message)
            status_code = 200
        else:
            message = 'Issue when inserting cocktail in DB'
            logger.info(message)
            status_code = 500
    except (KeyError, ValueError):
        message = f'Error when making cocktail from dict : {cocktails_details}'
        status_code = 500

    resp = jsonify(message)
    resp.status_code = status_code
    return resp

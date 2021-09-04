import logging

from flask import Blueprint, jsonify, request
from flasgger import swag_from

from core.models.cocktail import Cocktail, COCKTAIL_TYPE_MAPPING, CocktailType
from core.models.enum import Collection
from core.persist import cocktails_repository
from core.services import search_service

from api.admin_interface.auth import auth_required
from api.docs.cocktail_docs import cocktail_get_specs_dict, cocktail_search_specs_dict

logger = logging.getLogger(__name__)

cocktails_blueprint = Blueprint('cocktails', __name__)


@swag_from(cocktail_get_specs_dict)
@cocktails_blueprint.route('', methods=['GET'])
def get_all_cocktails():
    cocktail_types = [COCKTAIL_TYPE_MAPPING.get(g_t, None) for g_t in request.args.getlist('type')]
    max_preparation_time = request.args.get("max_preparation_time", None)
    cocktails = cocktails_repository.list_by(types=cocktail_types if len(cocktail_types) > 0 else None,
                                             max_preparation_time=int(
                                                 max_preparation_time) if max_preparation_time is not None else None)
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


@swag_from(cocktail_search_specs_dict)
@cocktails_blueprint.route('/search', methods=['GET'])
def search_cocktails():
    # get args from request
    name = request.args.get("name", None)
    cocktails = search_service.search_by_name(searched_name=name, collection=Collection.Cocktails)
    response = []
    for cocktail in cocktails:
        cocktail_obj = cocktail.to_dict()
        response.append(cocktail_obj)
    return jsonify(response)

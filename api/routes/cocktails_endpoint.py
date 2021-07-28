import logging

from flask import Blueprint, jsonify, request

from core.models.cocktail import Cocktail, COCKTAIL_TYPE_MAPPING
from core.persist import cocktails_repository

logger = logging.getLogger(__name__)

cocktails_blueprint = Blueprint('cocktails', __name__)


@cocktails_blueprint.route('', methods=['GET'])
def get_all_cocktails():
    cocktails = cocktails_repository.find_all_types()
    response = []
    for cocktail in cocktails:
        cocktail_obj = cocktail.to_dict()
        response.append(cocktail_obj)
    return jsonify(response)


@cocktails_blueprint.route('', methods=['POST'])
def create_cocktail():
    cocktails_details = request.json
    try:
        cocktail = Cocktail(
            name=cocktails_details["name"],
            description=cocktails_details["description"],
            ingredients=cocktails_details["ingredients"],
            preparation_time_min=cocktails_details["preparation_time_min"],
            image=cocktails_details["image"],
            cocktail_type=COCKTAIL_TYPE_MAPPING[cocktails_details["cocktail_type"]],
        )
        res = cocktails_repository.create_one(cocktail)
        if str(res.inserted_id) == str(cocktail._id):
            resp = jsonify('Cocktail added successfully')
            resp.status_code = 200
        else:
            resp = jsonify('Issue when inserting cocktail in DB')
            resp.status_code = 500
    except (KeyError, ValueError):
        logger.warning(f'error when making cocktail from dict : {cocktails_details}')
        resp = jsonify('Issue encountered when inserting cocktail')
        resp.status_code = 500

    return resp

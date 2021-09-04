import logging

from flask import Blueprint, jsonify, request
from flasgger import swag_from

from core.models.beer import Beer, BEER_TYPE_MAPPING, BeerType, BeerCategory, BEER_CATEGORY_MAPPING
from core.models.enum import Collection
from core.persist import beers_repository
from core.services import search_service

from api.docs.beer_docs import beer_get_specs_dict, beer_search_specs_dict
from api.admin_interface.auth import auth_required

logger = logging.getLogger(__name__)

beers_blueprint = Blueprint('beers', __name__)


@swag_from(beer_get_specs_dict)
@beers_blueprint.route('', methods=['GET'])
def get_all_beers():
    # get args from request
    beer_types = [BEER_TYPE_MAPPING.get(g_t, None) for g_t in request.args.getlist('type')]
    beer_categories = [BEER_CATEGORY_MAPPING.get(g_t, None) for g_t in request.args.getlist('category')]
    max_price = request.args.get("max_price", None)
    beers = beers_repository.list_by(beer_types=beer_types,
                                     categories=beer_categories,
                                     max_price=int(
                                         max_price) if max_price is not None else None)
    response = []
    for beer in beers:
        beer_obj = beer.to_dict()
        response.append(beer_obj)
    return jsonify(response)


@beers_blueprint.route('', methods=['POST'])
@auth_required
def create_beer():
    beers_details = request.json
    try:
        beer = Beer(
            name=beers_details.get("name"),
            description=beers_details.get("description"),
            price=beers_details.get("price"),
            alcohol_percentage=beers_details.get("alcohol_percentage"),
            category=BEER_CATEGORY_MAPPING[beers_details.get("category", BeerCategory.Other)],
            image=beers_details.get("image"),
            beer_type=BEER_TYPE_MAPPING[beers_details.get("beer_type", BeerType.Blond)],
        )
        logger.info(f'Inserting beer {beer.name} in DB')
        res = beers_repository.create_one(beer)
        if str(res.inserted_id) == str(beer._id):
            message = 'Beer added successfully'
            logger.info(message)
            status_code = 200
        else:
            message = 'Issue when inserting beer in DB'
            logger.warning(message)
            status_code = 500
    except (KeyError, ValueError) as err:
        logger.warning(f'error when making beer from dict : {beers_details} \n'
                       f'error : {err}')
        message = 'Issue encountered when inserting beer'
        status_code = 500

    resp = jsonify(message)
    resp.status_code = status_code
    return resp


@swag_from(beer_search_specs_dict)
@beers_blueprint.route('/search', methods=['GET'])
def search_beers():
    # get args from request
    name = request.args.get("name", None)
    beers = search_service.search_by_name(searched_name=name, collection=Collection.Beers)
    response = []
    for beer in beers:
        beer_obj = beer.to_dict()
        response.append(beer_obj)
    return jsonify(response)

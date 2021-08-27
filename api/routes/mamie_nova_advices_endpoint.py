import logging

from flask import Blueprint, jsonify, request

from core.models.mamie_nova_advice import MamieNovaAdvice, MAMIE_NOVA_ADVICE_TYPE_MAPPING, MamieNovaAdviceType
from core.persist import mamie_nova_advices_repository
from api.admin_interface.auth import auth_required

logger = logging.getLogger(__name__)

mamie_nova_advices_blueprint = Blueprint('mamie_nova_advices', __name__)


@mamie_nova_advices_blueprint.route('', methods=['GET'])
def get_all_mamie_nova_advices():
    # get args from request
    mamie_nova_advice_types = [MAMIE_NOVA_ADVICE_TYPE_MAPPING.get(g_t, None) for g_t in request.args.getlist('type')]
    mamie_nova_advices = mamie_nova_advices_repository.list_by(mamie_nova_advice_types=mamie_nova_advice_types)
    response = []
    for mamie_nova_advice in mamie_nova_advices:
        mamie_nova_advice_obj = mamie_nova_advice.to_dict()
        response.append(mamie_nova_advice_obj)
    return jsonify(response)


@mamie_nova_advices_blueprint.route('', methods=['POST'])
@auth_required
def create_mamie_nova_advice():
    mamie_nova_advices_details = request.json
    try:
        mamie_nova_advice = MamieNovaAdvice(
            name=mamie_nova_advices_details.get("name"),
            description=mamie_nova_advices_details.get("description"),
            links=mamie_nova_advices_details.get("links"),
            image=mamie_nova_advices_details.get("image"),
            mamie_nova_advice_type=MAMIE_NOVA_ADVICE_TYPE_MAPPING[
                mamie_nova_advices_details.get("mamie_nova_advice_type", MamieNovaAdviceType.Other)],
        )
        logger.info(f'Inserting mamie_nova_advice {mamie_nova_advice.name} in DB')
        res = mamie_nova_advices_repository.create_one(mamie_nova_advice)
        if str(res.inserted_id) == str(mamie_nova_advice._id):
            message = 'MamieNovaAdvice added successfully'
            logger.info(message)
            status_code = 200
        else:
            message = 'Issue when inserting mamie_nova_advice in DB'
            logger.warning(message)
            status_code = 500
    except (KeyError, ValueError) as err:
        logger.warning(f'error when making mamie_nova_advice from dict : {mamie_nova_advices_details} \n'
                       f'error : {err}')
        message = 'Issue encountered when inserting mamie_nova_advice'
        status_code = 500

    resp = jsonify(message)
    resp.status_code = status_code
    return resp

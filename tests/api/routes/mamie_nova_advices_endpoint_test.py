from core.models.mamie_nova_advice import MamieNovaAdvice, MamieNovaAdviceType
from tests.core.persist import utils
from tests.utils import one_of
from tests.fixtures.app import client


def test_list_mamie_nova_advices(client):
    new_mamie_nova_advice = utils.new_mamie_nova_advice()
    response = client.get('/mamie_nova_advices')
    assert response.status_code == 200
    mamie_nova_advices = [MamieNovaAdvice.from_db(d) for d in response.get_json()]
    assert new_mamie_nova_advice in mamie_nova_advices


def test_list_mamie_nova_advices_by_mamie_nova_advice_type(client):
    mamie_nova_advice_type = one_of(MamieNovaAdviceType)
    new_mamie_nova_advice = utils.new_mamie_nova_advice(mamie_nova_advice_type=mamie_nova_advice_type)
    response = client.get(f'/mamie_nova_advices?type={mamie_nova_advice_type.value}')
    assert response.status_code == 200
    mamie_nova_advices = [MamieNovaAdvice.from_db(d) for d in response.get_json()]
    assert new_mamie_nova_advice in mamie_nova_advices
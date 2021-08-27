from core.models.mamie_nova_advice import MamieNovaAdvice, MamieNovaAdviceType
from core.persist import mamie_nova_advices_repository
from tests.core.persist import utils
from tests.utils import list_of, one_of


def test_create_one():
    mamie_nova_advice = MamieNovaAdvice()
    result = mamie_nova_advices_repository.create_one(mamie_nova_advice)
    assert result.inserted_id == str(mamie_nova_advice._id)


def test_find_by_id():
    mamie_nova_advice = utils.new_mamie_nova_advice()
    db_mamie_nova_advice = mamie_nova_advices_repository.find_by(mamie_nova_advice._id)
    assert db_mamie_nova_advice == mamie_nova_advice


def test_list_by_all():
    mamie_nova_advices = list_of(utils.new_mamie_nova_advice, min_count=3)
    retrieved_mamie_nova_advices = mamie_nova_advices_repository.list_by()
    for mamie_nova_advice in mamie_nova_advices:
        assert mamie_nova_advice in retrieved_mamie_nova_advices


def test_list_by_mamie_nova_advice_type():
    my_mamie_nova_advice_type = one_of(MamieNovaAdviceType)
    good_mamie_nova_advices = list_of(
        lambda: utils.new_mamie_nova_advice(mamie_nova_advice_type=my_mamie_nova_advice_type), min_count=3)
    not_good_mamie_nova_advices = list_of(
        lambda: utils.new_mamie_nova_advice(mamie_nova_advice_type=one_of(MamieNovaAdviceType,
                                                                          excluding=[my_mamie_nova_advice_type])))
    retrieved_mamie_nova_advices = mamie_nova_advices_repository.list_by(
        mamie_nova_advice_types=[my_mamie_nova_advice_type])
    for mamie_nova_advice in good_mamie_nova_advices:
        assert mamie_nova_advice in retrieved_mamie_nova_advices
    for mamie_nova_advice in not_good_mamie_nova_advices:
        assert mamie_nova_advice not in retrieved_mamie_nova_advices
    for mamie_nova_advice in retrieved_mamie_nova_advices:
        assert mamie_nova_advice.mamie_nova_advice_type == my_mamie_nova_advice_type


def test_delete_by():
    mamie_nova_advices = list_of(lambda: utils.new_mamie_nova_advice())
    result = mamie_nova_advices_repository.delete_by([g._id for g in mamie_nova_advices])
    assert result.deleted_count == len(mamie_nova_advices)


def test_delete_all():
    _ = mamie_nova_advices_repository.delete_by()
    retrieved_mamie_nova_advices = mamie_nova_advices_repository.list_by()
    assert len(retrieved_mamie_nova_advices) == 0

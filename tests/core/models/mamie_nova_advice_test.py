from core.models.mamie_nova_advice import *


def test_dict_are_complete():
    for mamie_nova_advice_type in MamieNovaAdviceType:
        assert mamie_nova_advice_type in MAMIE_NOVA_ADVICE_TYPE_MAPPING.values()
        assert DEFAULT_IMAGE is not None

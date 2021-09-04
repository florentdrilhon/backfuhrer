from core.models.mamie_nova_advice import MamieNovaAdviceType

mamie_nova_advice_model = {"MamieNovaAdvice":
    {
        "type": "object",
        "properties": {
            "_id": {"type": "UUID"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "links": {"type": "object",
                            "properties": {"link_name": {"type": "string"}, "link": {"type": "string"}}},
            "mamie_nova_advice_type": {"type": "string", "enum": [m_t.value for m_t in MamieNovaAdviceType], },
            "image": {"type": "string"},
            "created_at": {"type": "datetime"},
            "updated_at": {"type": "datetime"},
        }
    }
}

mamie_nova_advice_get_specs_dict = {
    "parameters": [
        {
            "name": "type",
            "in": "path",
            "type": "string",
            "enum": [m_t.value for m_t in MamieNovaAdviceType],
            "required": "false",
            "default": "all"
        }
    ],
    "definitions": mamie_nova_advice_model,
    "responses": {
        "200": {
            "description": "A list of mamie_nova_advices (may be filtered by type)",
            "schema": {
                "$ref": "#/definitions/MamieNovaAdvice"
            }
        }
    }
}

mamie_nova_advice_search_specs_dict = {
    "parameters": [
        {
            "name": "name",
            "in": "path",
            "type": "string",
            "required": "true"
        }
    ],
    "definitions": mamie_nova_advice_model,
    "responses": {
        "200": {
            "description": "A list of mamie_nova_advices searched by name",
            "schema": {
                "$ref": "#/definitions/MamieNovaAdvice"
            }
        }
    }
}

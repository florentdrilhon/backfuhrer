from core.models.beer import BeerType, BeerCategory

beer_model = {"Beer":
    {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "detailed_description": {"type": "string"},
            "price": {"type": "integer"},
            "alcohol_percentage": {"type": "integer"},
            "beer_type": {"type": "string", "enum": [g_t.value for g_t in BeerType], },
            "category": {"type": "string", "enum": [g_t.value for g_t in BeerCategory], },
            "image": {"type": "string"},
            "created_at": {"type": "datetime"},
            "updated_at": {"type": "datetime"},
        }
    }
}

beer_get_specs_dict = {
    "parameters": [
        {
            "name": "type",
            "in": "path",
            "type": "string",
            "enum": [g_t.value for g_t in BeerType],
            "required": "false",
            "default": "all"
        },
        {
            "name": "category",
            "in": "path",
            "type": "string",
            "enum": [g_t.value for g_t in BeerCategory],
            "required": "false",
            "default": "all"
        },
        {
            "name": "max_price",
            "in": "path",
            "type": "integer",
            "required": "false"
        }
    ],
    "definitions": beer_model,
    "responses": {
        "200": {
            "description": "A list of beers (may be filtered by type, category or price)",
            "schema": {
                "$ref": "#/definitions/Beer"
            }
        }
    }
}

beer_search_specs_dict = {
    "parameters": [
        {
            "name": "name",
            "in": "path",
            "type": "string",
            "required": "true"
        }
    ],
    "definitions": beer_model,
    "responses": {
        "200": {
            "description": "A list of beers searched by name",
            "schema": {
                "$ref": "#/definitions/Beer"
            }
        }
    }
}

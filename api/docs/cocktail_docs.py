from core.models.cocktail import CocktailType

cocktail_model = {"Cocktail":
    {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "description": {"type": "string"},
            "recipe": {"type": "array", "items": {"type": "string"}},
            "ingredients": {"type": "object",
                            "properties": {"ingredient_name": {"type": "string"}, "quantity": {"type": "string"}}},
            "preparation_time_min": {"type": "integer"},
            "cocktail_type": {"type": "string", "enum": [g_t.value for g_t in CocktailType], },
            "image": {"type": "string"},
            "created_at": {"type": "datetime"},
            "updated_at": {"type": "datetime"},
        }
    }
}

cocktail_get_specs_dict = {
    "parameters": [
        {
            "name": "type",
            "in": "path",
            "type": "string",
            "enum": [g_t.value for g_t in CocktailType],
            "required": "false",
            "default": "all"
        },
        {
            "name": "max_preparation_time",
            "in": "path",
            "type": "integer",
            "required": "false"
        }
    ],
    "definitions": cocktail_model,
    "responses": {
        "200": {
            "description": "A list of cocktails (may be filtered by type, or preparation time)",
            "schema": {
                "$ref": "#/definitions/Cocktail"
            }
        }
    }
}

cocktail_search_specs_dict = {
    "parameters": [
        {
            "name": "name",
            "in": "path",
            "type": "string",
            "required": "true"
        }
    ],
    "definitions": cocktail_model,
    "responses": {
        "200": {
            "description": "A list of cocktails searched by name",
            "schema": {
                "$ref": "#/definitions/Cocktail"
            }
        }
    }
}

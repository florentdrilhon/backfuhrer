from core.models.game import GameType

game_model = {"Game":
    {
        "type": "object",
        "properties": {
            "_id": {"type": "UUID"},
            "name": {"type": "string"},
            "description": {"type": "string"},
            "rules": {"type": "string"},
            "duration_min": {"type": "integer"},
            "game_type": {"type": "string", "enum": [g_t.value for g_t in GameType], },
            "number_of_players": {"type": "array", "items": {"type": "integer"}, "minItems": 1, "maxItems": 2},
            "image": {"type": "string"},
            "created_at": {"type": "datetime"},
            "updated_at": {"type": "datetime"},
        }
    }
}

game_get_specs_dict = {
    "parameters": [
        {
            "name": "type",
            "in": "path",
            "type": "string",
            "enum": [g_t.value for g_t in GameType],
            "required": "false",
            "default": "all"
        },
        {
            "name": "number_players",
            "in": "path",
            "type": "integer",
            "required": "false"
        }
    ],
    "definitions": game_model,
    "responses": {
        "200": {
            "description": "A list of games (may be filtered by type, number of players)",
            "schema": {
                "$ref": "#/definitions/Game"
            }
        }
    }
}

game_search_specs_dict = {
    "parameters": [
        {
            "name": "name",
            "in": "path",
            "type": "string",
            "required": "true"
        }
    ],
    "definitions": game_model,
    "responses": {
        "200": {
            "description": "A list of games searched by name",
            "schema": {
                "$ref": "#/definitions/Game"
            }
        }
    }
}

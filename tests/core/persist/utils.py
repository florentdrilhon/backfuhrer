from typing import Optional, Tuple, Dict

from core.models.game import Game, GameType
from core.models.cocktail import Cocktail, CocktailType
from core.persist import games_repository, cocktails_repository
from tests.utils import random_string, random_number, one_of


def new_game(name: Optional[str] = None,
             description: Optional[str] = None,
             rules: Optional[str] = None,
             duration_min: Optional[int] = None,
             number_of_players: Optional[Tuple[int, int]] = None,
             image: Optional[str] = None,
             game_type: Optional[GameType] = None) -> Game:
    game = Game()
    game.name = name or random_string()
    game.description = description or random_string()
    game.rules = rules or random_string()
    game.duration_min = duration_min or random_number(10, 60)
    game.number_of_players = number_of_players or (random_number(1, 5), random_number(6, 10))
    game.image = image or random_string()
    game.game_type = game_type or one_of(GameType)
    games_repository.create_one(game)
    return game


def new_cocktail(name: Optional[str] = None,
                 ingredients: Optional[Dict[str, str]] = None,
                 description: Optional[str] = None,
                 preparation_time_min: Optional[int] = None,
                 image: Optional[str] = None,
                 cocktail_type: Optional[CocktailType] = None) -> Cocktail:
    cocktail = Cocktail()
    cocktail.name = name or random_string()
    cocktail.ingredients = ingredients or {random_string(5,10) : random_string(5,10)}
    cocktail.description = description or random_string()
    cocktail.preparation_time_min = preparation_time_min or random_number(10, 60)
    cocktail.image = image or random_string()
    cocktail.cocktail_type = cocktail_type or one_of(CocktailType)
    cocktails_repository.create_one(cocktail)
    return cocktail

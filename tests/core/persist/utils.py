from typing import Optional, Tuple, Dict, List

from core.models.beer import BeerCategory, BeerType, Beer
from core.models.game import Game, GameType
from core.models.cocktail import Cocktail, CocktailType
from core.models.mamie_nova_advice import MamieNovaAdvice, MamieNovaAdviceType
from core.persist import games_repository, cocktails_repository, beers_repository, mamie_nova_advices_repository
from tests.utils import random_number, one_of, ascii_string


def new_game(name: Optional[str] = None,
             description: Optional[str] = None,
             rules: Optional[str] = None,
             duration_min: Optional[int] = None,
             number_of_players: Optional[Tuple[int, int]] = None,
             image: Optional[str] = None,
             game_type: Optional[GameType] = None) -> Game:
    game = Game()
    game.name = name or ascii_string()
    game.description = description or ascii_string()
    game.rules = rules or ascii_string()
    game.duration_min = duration_min or random_number(10, 60)
    game.number_of_players = number_of_players or (random_number(1, 5), random_number(6, 10))
    game.image = image or ascii_string()
    game.game_type = game_type or one_of(GameType)
    games_repository.create_one(game)
    return game


def new_cocktail(name: Optional[str] = None,
                 ingredients: Optional[Dict[str, str]] = None,
                 description: Optional[str] = None,
                 recipe: Optional[List[str]] = None,
                 preparation_time_min: Optional[int] = None,
                 image: Optional[str] = None,
                 cocktail_type: Optional[CocktailType] = None) -> Cocktail:
    cocktail = Cocktail()
    cocktail.name = name or ascii_string()
    cocktail.ingredients = ingredients or {ascii_string(5, 10): ascii_string(5, 10)}
    cocktail.description = description or ascii_string()
    cocktail.recipe = recipe or [ascii_string(10) for _ in range(random_number(1, 6))]
    cocktail.preparation_time_min = preparation_time_min or random_number(10, 60)
    cocktail.image = image or ascii_string()
    cocktail.cocktail_type = cocktail_type or one_of(CocktailType)
    cocktails_repository.create_one(cocktail)
    return cocktail


def new_beer(name: Optional[str] = None,
             description: Optional[str] = None,
             price: Optional[float] = None,
             alcohol_percentage: Optional[float] = None,
             category: Optional[BeerCategory] = None,
             image: Optional[str] = None,
             beer_type: Optional[BeerType] = None) -> Beer:
    beer = Beer()
    beer.name = name or ascii_string()
    beer.description = description or ascii_string()
    beer.price = price or random_number(10, 60)
    beer.alcohol_percentage = alcohol_percentage or random_number(0, 60)
    beer.image = image or ascii_string()
    beer.beer_type = beer_type or one_of(BeerType)
    beer.category = category or one_of(BeerCategory)
    beers_repository.create_one(beer)
    return beer


def new_mamie_nova_advice(name: Optional[str] = None,
                          description: Optional[str] = None,
                          image: Optional[str] = None,
                          mamie_nova_advice_type: Optional[BeerType] = None,
                          links: Optional[Dict[str, str]] = None) -> MamieNovaAdvice:
    mamie_nova_advice = MamieNovaAdvice()
    mamie_nova_advice.name = name or ascii_string()
    mamie_nova_advice.description = description or ascii_string()
    mamie_nova_advice.image = image or ascii_string()
    mamie_nova_advice.mamie_nova_advice_type = mamie_nova_advice_type or one_of(MamieNovaAdviceType)
    mamie_nova_advice.links = links or {ascii_string(): ascii_string()}
    mamie_nova_advices_repository.create_one(mamie_nova_advice)
    return mamie_nova_advice

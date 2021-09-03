from enum import Enum
from core.models.game import Game
from core.models.beer import Beer
from core.models.cocktail import Cocktail
from core.models.mamie_nova_advice import MamieNovaAdvice


class Collection(Enum):
    Beers = 'beers'
    Cocktails = 'cocktails'
    Games = 'games'
    MamieNovaAdvices = 'mamie_nova_advices'


class Entity(Enum):
    Game = Game
    Beer = Beer
    Cocktail = Cocktail
    MamieNovaAdvice = MamieNovaAdvice

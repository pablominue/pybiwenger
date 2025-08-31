import dotenv

from pybiwenger.src.biwenger.players import Player, PlayersAPI
from tests.data import PLAYERS

dotenv.load_dotenv()

import pybiwenger

pybiwenger.authenticate()

print(pybiwenger.PlayersAPI().user_league)

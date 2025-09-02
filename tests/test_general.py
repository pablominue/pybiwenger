import os
import pprint

import pybiwenger
from pybiwenger.src.biwenger.players import PlayersAPI
from pybiwenger.src.client import BiwengerBaseClient

os.environ["BIWENGER_LEAGUE"] = "SIMPS"

client = BiwengerBaseClient()

players_api = PlayersAPI()
all_players = players_api.get_all_players()

catena = next((x for x in all_players if x.name == "Catena"), None)

catena_history = players_api.get_player_history(catena)

pprint.pprint(catena_history)

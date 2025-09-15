import os
import random
import time

from pybiwenger.src.biwenger.players import PlayersAPI
from pybiwenger.utils.exporting import Exporting
from pybiwenger.utils.parsing import Parsing

os.environ["BIWENGER_LEAGUE"] = "SIMPS"
# os.environ["BIWENGER_PROXY"] = "" #Include the proxy URL if you want to use one

players_api = PlayersAPI()
all_players = players_api.get_all_players()

my_user = ""  # Fill with your Linux user

path = f"/home/{my_user}/biwenger_players_market_data/"

for player in all_players:

    market_history = players_api.get_market_history(player)

    path_specific = path + f"{player.slug}.csv"
    Exporting.exporting_list_dicts_to_csv(market_history, path_specific)

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

path = f"/home/{my_user}/biwenger_players_history_data_WITH_DATE/"

years_to_get = ["2025", "2024", "2023", "2022", "2021", "2020", "2019", "2018"]

for year in years_to_get:
    for player in all_players:

        points_history = players_api.get_points_history(player, year)
        enriched_info = Parsing.enrich_and_parse_points_history_info(
            points_history, player, year
        )

        renamed_enriched_info = Parsing.rename_points_history_dict(enriched_info)

        path_specific = path + f"{player.slug}-{year}.csv"
        Exporting.exporting_list_dicts_to_csv(renamed_enriched_info, path_specific)

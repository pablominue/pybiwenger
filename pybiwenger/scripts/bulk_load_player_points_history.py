import os
from pybiwenger.src.biwenger.players import PlayersAPI
from pybiwenger.utils.parsing import Parsing
from pybiwenger.utils.exporting import Exporting
import time
import random


os.environ["BIWENGER_LEAGUE"] = "SIMPS"

players_api = PlayersAPI()
all_players = players_api.get_all_players()

my_user = "victu" #Fill with your Linux user

path = f"/home/{my_user}/biwenger_players_history_data/"

years_to_get = ["2025","2024","2023","2022","2021","2020","2019","2018"]

for player in all_players:
    for year in years_to_get:

        points_history = players_api.get_points_history(player, year)
        enriched_info = Parsing.enrich_and_parse_points_history_info(points_history, player, year)

        renamed_enriched_info = Parsing.rename_points_history_dict(enriched_info)

        path_specific = path + f"{player.slug}-{year}.csv"
        Exporting.exporting_list_dicts_to_csv(renamed_enriched_info, path_specific)

        time.sleep(random.uniform(1, 1.25))


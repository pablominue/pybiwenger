import os
import random
import time

from pybiwenger.src.biwenger.players import PlayersAPI
from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.utils.parsing import Parsing

class Endpoints():

    os.environ["BIWENGER_LEAGUE"] = "SIMPS"
    # os.environ["BIWENGER_PROXY"] = "" #Include the proxy URL if you want to use one

    def daily_squad_market_endpoint():

        client = BiwengerBaseClient()

        players_api = PlayersAPI()
        roster = players_api.get_user_roster(client.user.id)
        players = roster.players

        for player in players:
            points_history = players_api.get_points_history_for_inference(player, "2026")
            enriched_info = Parsing.enrich_and_parse_points_history_info_for_inference(
                points_history, player, "2026"
            )
            renamed_enriched_info = Parsing.rename_points_history_dict_for_inference(enriched_info)
            pass

Endpoints.daily_squad_market_endpoint()            



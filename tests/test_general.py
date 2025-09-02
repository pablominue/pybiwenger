import os
import pprint

import polars as pl

import pybiwenger
from pybiwenger.src.biwenger.players import PlayersAPI
from pybiwenger.src.client import BiwengerBaseClient

os.environ["BIWENGER_LEAGUE"] = "SIMPS"

client = BiwengerBaseClient()

players_api = PlayersAPI()


def test_catena():
    all_players = players_api.get_all_players()

    catena = next((x for x in all_players if x.name == "Catena"), None)

    catena_history = players_api.get_player_history(catena)

    assert len(catena_history) > 0


def test_polars():
    all_players = players_api.get_all_players()
    df = pybiwenger.players_to_polars(all_players)
    assert isinstance(df, pl.DataFrame)

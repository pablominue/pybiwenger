from pydantic import BaseModel

from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.src.client.urls import url_all_players, url_players_league
from pybiwenger.utils.log import PabLog

lg = PabLog(__name__)

class Player(BaseModel):
    pass


class Players(BiwengerBaseClient):
    def __init__(self) -> None:
        super().__init__()
        self._league_player_url = url_players_league
        self._all_players_url = url_all_players
        self.players = self._get_all_players()

    def _get_all_players(self) -> dict:
        data = self.fetch(self._all_players_url)
        return data

    def get_my_players(self) -> dict:
        res = self.fetch(self._league_player_url, league_headers=False)
        if not res:
            return {}
        if not res.get("data"):
            return {}
        if not res["data"].get("players"):
            return {}
        data = res["data"]["players"]
        return data

from pydantic import BaseModel

from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.types.account import AccountData
from pybiwenger.src.client.urls import url_all_players, url_league
from pybiwenger.utils.log import PabLog

lg = PabLog(__name__)

class Player(BaseModel):
    pass


class Players(BiwengerBaseClient):
    def __init__(self) -> None:
        super().__init__()
        self._league_url = url_league + str(self.account.leagues[0].id)
        self._all_players_url = url_all_players
        self.players = self._get_all_players()

    def _get_all_players(self) -> dict:
        data = self.fetch(self._all_players_url)
        return data


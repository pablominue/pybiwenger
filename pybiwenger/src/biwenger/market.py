import typing as t

from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.src.client.urls import url_players_market
from pybiwenger.utils.log import PabLog


class Market(BiwengerBaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.url = url_players_market

    def get_market_data(self) -> t.Optional[dict]:
        return self.fetch(self.url)

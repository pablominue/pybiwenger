"""Market module for Biwenger API.

Provides access to the market data for players in the selected league.
"""

import typing as t

from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.src.client.urls import url_players_market
from pybiwenger.utils.log import PabLog


class MarketAPI(BiwengerBaseClient):
    """Client for retrieving market data from the Biwenger API."""

    def __init__(self) -> None:
        super().__init__()
        self.url = url_players_market

    def get_market_data(self) -> t.Optional[dict]:
        """Fetches market data for players.

        Returns:
            Optional[dict]: The market data if successful, None otherwise.
        """
        return self.fetch(self.url)

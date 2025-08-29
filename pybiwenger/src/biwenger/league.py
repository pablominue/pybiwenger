"""League module for Biwenger API.

Provides access to league information and users.
"""

import json
import typing as t

from pydantic import BaseModel

from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.src.client.urls import url_all_players, url_league
from pybiwenger.types.account import AccountData
from pybiwenger.types.user import User
from pybiwenger.utils.log import PabLog


class LeagueAPI(BiwengerBaseClient):
    """Client for retrieving league information from the Biwenger API."""

    def __init__(self) -> None:
        super().__init__()
        self._league_url = url_league + str(self.account.leagues[0].id)

    def get_users(self) -> t.Iterable[User]:
        """Fetches all users in the league.

        Returns:
            Iterable[User]: List of users in the league.
        """
        data = self.fetch(self._league_url)["data"]
        print(data)
        users = [
            User.model_validate_json(json.dumps(player))
            for player in data.get("users", [])
        ]
        return users

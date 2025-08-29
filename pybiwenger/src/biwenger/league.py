from pydantic import BaseModel

from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.types.account import AccountData
from pybiwenger.types.user import User
from pybiwenger.src.client.urls import url_all_players, url_league
from pybiwenger.utils.log import PabLog
import typing as t
import json


class League(BiwengerBaseClient):
    def __init__(self) -> None:
        super().__init__()
        self._league_url = url_league + str(self.account.leagues[0].id)
        self.users: t.Iterable[User] = self._get_users()

    def _get_users(self) -> t.Iterable[User]:
        data = self.fetch(self._league_url)['data']
        print(data)
        users = [User.model_validate_json(json.dumps(player)) for player in data.get("users", [])]
        return users
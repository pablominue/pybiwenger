"""Client module for Biwenger API interaction.

Handles authentication, session management, and basic API requests for Biwenger.
"""

import json
import os
import typing as t

import requests
from pydantic import BaseModel
from retry import retry

from pybiwenger.src.client.urls import (url_account, url_competitions,
                                        url_login, url_user)
from pybiwenger.types.account import *
from pybiwenger.types.account import League
from pybiwenger.types.player import Player
from pybiwenger.types.user import Team, User
from pybiwenger.utils.log import PabLog

lg = PabLog(__name__)


class BiwengerAuthError(Exception):
    """Custom exception for Biwenger authentication errors."""

    pass


class BiwengerError(Exception):
    pass


class BiwengerBaseClient:
    def __init__(self) -> None:
        """Initializes the BiwengerBaseClient.

        Loads credentials from environment variables, authenticates, and sets up session headers.
        """
        if os.getenv("BIWENGER_USERNAME") and os.getenv("BIWENGER_PASSWORD"):
            self.username = os.getenv("BIWENGER_USERNAME")
            self.password = os.getenv("BIWENGER_PASSWORD")
        else:
            raise BiwengerAuthError(
                "Environment variables BIWENGER_USERNAME and BIWENGER_PASSWORD must be set. Use biwenger.authenticate() function."
            )
        self.authenticated = False
        self.auth: t.Optional[str] = None
        self.token: t.Optional[str] = None
        self.__refresh_token()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "X-Lang": "es",
                "Authorization": self.auth,
            }
        )
        self.account: AccountData = self.__get_account_info()

    @property
    def user_league(self) -> League:
        return self.account.leagues

    @user_league.setter
    def user_league(self) -> None:
        return BiwengerError("User League can not be overwriteen")

    @property
    def user(self):
        return self.account.leagues[0].user.to_user()

    @user.setter
    def user(self) -> None:
        return BiwengerError("User can not be overwriteen")

    @property
    def user_team(self) -> Team:
        owner = self.user
        players = self._get_my_players_enriched()
        return Team(owner=owner, players=players)

    @user_team.setter
    def user_team(self) -> None:
        return BiwengerError("User League can not be overwriteen")

    def __get_my_player_ids(self) -> list[int]:
        url = url_user
        data = self.fetch(f"{url}?fields=players(id,owner)") or {}
        players = (data.get("data") or {}).get("players", [])
        return [int(p["id"]) for p in players]

    def __get_catalog(
        self, competition: t.Optional[str] = "la-liga"
    ) -> dict[str, dict]:
        url = url_competitions + f"{competition}/data"
        cat = self.fetch(f"{url}?lang=es&score=5")
        return (cat or {}).get("data", {}).get("players", {})

    def __get_my_players_enriched(self) -> list[Player]:
        my_ids = self.__get_my_player_ids()
        catalog = self.__get_catalog()

        players = []
        for pid in my_ids:
            raw = catalog.get(str(pid))
            if raw:
                raw["id"] = pid
                players.append(Player.model_validate(raw))
            else:
                players.append(Player(id=pid, name=f"Unknown_{pid}"))

        return players

    def __refresh_token(self) -> None:
        """Refreshes the authentication token by logging in to the Biwenger API.

        Raises:
            BiwengerAuthError: If login fails due to invalid credentials.
        """

        lg.log.info("Login process")
        data = {"email": self.username, "password": self.password}
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json, text/plain, */*",
        }
        contents = requests.post(
            url_login, data=json.dumps(data), headers=headers
        ).json()
        if "token" in contents:
            lg.log.info("Login successful")
            self.token = contents["token"]
            self.auth = "Bearer " + self.token
            self.authenticated = True
            return
        else:
            raise BiwengerAuthError("Login failed, check your credentials.")

    def __get_account_info(self, league_name: t.Optional[str] = None) -> AccountData:
        """Fetches account information from the Biwenger API.

        Args:
            league_name (Optional[str]): Name of the league to select.

        Returns:
            AccountData: Parsed account data from the API.
        """
        result = requests.get(url_account, headers=self.session.headers).json()
        if result["status"] == 200:
            lg.log.info("call login ok!")
        else:
            lg.log.error(result["message"])
        if league_name is not None:
            os.environ["BIWENGER_LEAGUE_NAME"] = league_name
        else:
            os.environ["BIWENGER_LEAGUE_NAME"] = result["data"]["leagues"][0]["name"]
        league_info = [
            x
            for x in result["data"]["leagues"]
            if x["name"] == os.getenv("BIWENGER_LEAGUE_NAME")
        ][0]

        id_league = league_info["id"]
        id_user = league_info["user"]["id"]
        lg.log.info("Updating Headers with league and user info")
        self.session.headers.update(
            {
                "X-League": repr(id_league),
                "X-User": repr(id_user),
            }
        )
        if result["status"] == 200:
            lg.log.info("Account details fetched successfully.")
            return AccountData.model_validate_json(json.dumps(result["data"]))

    @retry(tries=3, delay=2)
    def fetch(self, url: str) -> t.Optional[dict]:
        """Fetches data from a given URL using the authenticated session.

        Args:
            url (str): The API endpoint to fetch data from.

        Returns:
            Optional[dict]: The response data if successful, None otherwise.
        """
        if not self.authenticated or self.auth is None:
            lg.log.info("Not authenticated, cannot fetch data.")
            return None
        response = requests.get(url, headers=self.session.headers)
        if response.status_code == 200:
            return response.json()
        else:
            lg.log.error(
                f"Failed to fetch data from {url}, status code: {response.status_code}"
            )
            lg.log.error(f"Response: {response.text}")
            return None

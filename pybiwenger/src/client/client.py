"""Client module for Biwenger API interaction.

Handles authentication, session management, and basic API requests for Biwenger.
"""

import json
import os
import typing as t

import requests
from pydantic import BaseModel
from retry import retry

from pybiwenger.src.client.urls import url_account, url_login
from pybiwenger.types.account import *
from pybiwenger.utils.log import PabLog

lg = PabLog(__name__)


class BiwengerAuthError(Exception):
    """Custom exception for Biwenger authentication errors."""

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
        self._refresh_token()
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Content-type": "application/json",
                "Accept": "application/json, text/plain, */*",
                "X-Lang": "es",
                "Authorization": self.auth,
            }
        )
        self.account: AccountData = self._get_account_info()

    def _refresh_token(self) -> None:
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

    def _get_account_info(self, league_name: t.Optional[str] = None) -> AccountData:
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

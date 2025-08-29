"""Client module for Biwenger API interaction."""

import json
import os
import typing as t

import requests
from retry import retry

from pybiwenger.src.client.urls import url_login, url_account
from pybiwenger.utils.log import PabLog

lg = PabLog(__name__)


class BiwengerAuthError(Exception):
    """Custom exception for Biwenger authentication errors."""

    pass


class BiwengerBaseClient:
    def __init__(self) -> None:
        if os.getenv("BIWENGER_USERNAME") and os.getenv("BIWENGER_PASSWORD"):
            self.username = os.getenv("BIWENGER_USERNAME")
            self.password = os.getenv("BIWENGER_PASSWORD")
        else:
            raise BiwengerAuthError(
                "Environment variables BIWENGER_USERNAME and BIWENGER_PASSWORD must be set. Use biwenger.authenticate() function."
            )
        self.authenticated = False
        self.auth: t.Optional[str] = None
        self.token: t.Optional[str] = self._refresh_token()
        self.headers = {
            "Content-type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "X-Lang": "es",
            "Authorization": self.auth,
        }

    def _refresh_token(self) -> t.Optional[str]:
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
            return contents["token"]
        else:
            raise BiwengerAuthError("Login failed, check your credentials.")

    def get_account_info(self):

        result = requests.get(url_account, headers=self.headers).json()
        if result["status"] == 200:
            lg.log.info("call login ok!")
        league_info = [
            x
            for x in result["data"]["leagues"]
            if x["name"] == os.getenv("BIWENGER_LEAGUE_NAME")
        ][0]
        id_league = league_info["id"]
        id_user = league_info["user"]["id"]
        headers_league = {
            "Content-type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "X-Lang": "es",
            "X-League": repr(id_league),
            "X-User": repr(id_user),
            "Authorization": self.auth,
        }
        if result["status"] == 200:
            lg.log.info("call login ok!")
            return result, headers_league

    @retry(tries=3, delay=2)
    def fetch(self, url: str) -> t.Optional[dict]:
        if not self.authenticated or self.auth is None:
            lg.log.info("Not authenticated, cannot fetch data.")
            return None
        headers = {
            "Content-type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "X-Lang": "es",
            "Authorization": self.auth,
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            lg.log.error(
                f"Failed to fetch data from {url}, status code: {response.status_code}"
            )
            lg.log.error(f"Response: {response.text}")
            return None

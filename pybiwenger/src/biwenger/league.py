"""League module for Biwenger API.

Provides access to league information and users.
"""

import json
import typing as t
from typing import Any, Dict, Iterable, List

from pydantic import BaseModel

from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.src.client.urls import url_league, url_rounds
from pybiwenger.types.account import AccountData
from pybiwenger.types.player import Player
from pybiwenger.types.user import Standing, User
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
        users = [
            User.model_validate_json(json.dumps(player))
            for player in data.get("users", [])
        ]
        return users

    def get_classification(self) -> List[Standing]:
        """Clasificación actual de la liga (posición y puntos por usuario)."""
        data = self.fetch(self._league_url) or {}
        league = data.get("data") or {}
        # En muchas respuestas, los usuarios traen puntos y posición actuales
        users = league.get("users", [])  # verificar estructura real en tu respuesta
        standings: List[Standing] = []
        for u in users:
            standings.append(
                Standing(
                    user_id=u.get("id"),
                    name=u.get("name"),
                    points=u.get("points", 0),
                    position=u.get("position", 0),
                )
            )
        # Si no vienen puntos/posición aquí, consultar rounds/league
        if not any(s.points for s in standings):
            rounds = self.fetch(url_rounds) or {}
            # Adaptar a la estructura real de la respuesta de rounds
            # ...
        return sorted(standings, key=lambda s: s.position or 9999)

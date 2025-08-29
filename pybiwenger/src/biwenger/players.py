from __future__ import annotations

import json
from collections import defaultdict
from typing import Any, DefaultDict, Dict, Iterable, List, Optional, Union

from pydantic import BaseModel, Field

from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.types.player import Player  # tu modelo completo
from pybiwenger.types.user import Team, User
from pybiwenger.utils.log import PabLog

lg = PabLog(__name__)


class PlayersAPI(BiwengerBaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.league_id = self.account.leagues.id
        self._users_players_url = (
            "https://biwenger.as.com/api/v2/user?fields=players(id,owner)"
        )
        self._catalog_url = (
            "https://biwenger.as.com/api/v2/competitions/la-liga/data?lang=es&score=5"
        )
        self._league_url = f"https://biwenger.as.com/api/v2/league/{self.league_id}"
        self._catalog = None
        self._users_index = None

    def get_users_players_raw(self) -> List[Dict[str, Any]]:
        data = self.fetch(self._users_players_url)
        return (data or {}).get("data", {}).get("players", [])

    def get_user_players_raw(self, owner_id: int) -> List[Dict[str, Any]]:
        return [p for p in self.get_users_players_raw() if p.get("owner") == owner_id]

    def get_catalog(self) -> Dict[str, Dict[str, Any]]:
        if self._catalog is None:
            cat = self.fetch(self._catalog_url)
            self._catalog = (cat or {}).get("data", {}).get("players", {})
        return self._catalog

    def get_league_users(self) -> List[User]:
        data = self.fetch(self._league_url) or {}
        users_raw = (data.get("data") or {}).get("users", [])
        return [User.model_validate_json(json.dumps(u)) for u in users_raw]

    def _users_by_id(self) -> Dict[int, User]:
        if self._users_index is None:
            self._users_index = {u.id: u for u in self.get_league_users()}
        return self._users_index

    def _enrich_player(self, pid: int) -> Player:
        cat = self.get_catalog()
        raw = cat.get(str(pid), {}) | {"id": pid}
        return Player.model_validate(raw)

    def get_user_roster(self, owner_id: int) -> Team:
        owner = self._users_by_id().get(owner_id)
        if owner is None:
            return Team(
                owner=User(id=owner_id, name=str(owner_id), icon=""), players=[]
            )
        player_ids = [int(p["id"]) for p in self.get_user_players_raw(owner_id)]
        players = [self._enrich_player(pid) for pid in player_ids]
        return Team(owner=owner, players=players)

    def get_rosters_by_owner(self) -> Dict[User, List[Player]]:
        pairs = self.get_users_players_raw()
        by_owner: DefaultDict[int, List[int]] = defaultdict(list)
        for p in pairs:
            by_owner[p["owner"]].append(int(p["id"]))
        users = self._users_by_id()
        result: Dict[User, List[Player]] = {}
        for oid, pids in by_owner.items():
            owner = users.get(oid, User(id=oid, name=str(oid), icon=""))
            result[owner] = [self._enrich_player(pid) for pid in pids]
        return result

    def get_team_ids(self, owner_id: int) -> List[int]:
        return [int(p["id"]) for p in self.get_user_players_raw(owner_id)]

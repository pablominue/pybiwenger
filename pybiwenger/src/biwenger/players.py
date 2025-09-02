from __future__ import annotations

import json
import typing as t
from collections import defaultdict
from datetime import datetime, timezone
from typing import (Any, DefaultDict, Dict, Iterable, List, Optional, Tuple,
                    Union)

from pydantic import BaseModel, Field

from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.src.client.urls import (url_catalog, url_competitions,
                                        url_league, url_user_players)
from pybiwenger.types.player import Player
from pybiwenger.types.user import Team, User
from pybiwenger.utils.log import PabLog

lg = PabLog(__name__)


class PlayersAPI(BiwengerBaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.league_id = self.account.leagues[0].id
        self._users_players_url = url_user_players
        self._catalog_url = url_catalog
        self._league_url = url_league[0] + str(self.league_id)
        self._catalog = None
        self._users_index = None

    def __get_users_players_raw(self) -> List[Dict[str, Any]]:
        data = self.fetch(self._users_players_url)
        return (data or {}).get("data", {}).get("players", [])

    def __get_user_players_raw(self, owner_id: int) -> List[Dict[str, Any]]:
        return [p for p in self.__get_users_players_raw() if p.get("owner") == owner_id]

    def __get_catalog(self) -> Dict[str, Dict[str, Any]]:
        if self._catalog is None:
            cat = self.fetch(self._catalog_url)
            self._catalog = (cat or {}).get("data", {}).get("players", {})
        return self._catalog

    def get_all_players(self) -> t.Iterable[Player]:
        catalog = self.__get_catalog()
        return [Player.model_validate(player) for player in catalog.values()]

    def get_league_users(self) -> List[User]:
        data = self.fetch(self._league_url) or {}
        users_raw = (data.get("data") or {}).get("users", [])
        return [User.model_validate_json(json.dumps(u)) for u in users_raw]

    def _users_by_id(self) -> Dict[int, User]:
        if self._users_index is None:
            self._users_index = {u.id: u for u in self.get_league_users()}
        return self._users_index

    def _enrich_player(self, pid: int) -> Player:
        cat = self.__get_catalog()
        raw = cat.get(str(pid), {}) | {"id": pid}
        return Player.model_validate(raw)

    def get_user_roster(self, owner_id: int) -> Team:
        owner = self._users_by_id().get(owner_id)
        if owner is None:
            return Team(
                owner=User(id=owner_id, name=str(owner_id), icon=""), players=[]
            )
        player_ids = [int(p["id"]) for p in self.__get_user_players_raw(owner_id)]
        players = [self._enrich_player(pid) for pid in player_ids]
        return Team(owner=owner, players=players)

    def get_rosters_by_owner(self) -> Dict[User, List[Player]]:
        pairs = self.__get_users_players_raw()
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
        return [int(p["id"]) for p in self.__get_user_players_raw(owner_id)]

    def _catalog_url_for(
        self, competition: str, score: int, season: Optional[int] = None
    ) -> str:
        base = url_competitions + "/" + f"{competition}/data"
        qs = {"lang": "es", "score": str(score)}
        if season is not None:
            qs["season"] = str(season)
        from urllib.parse import urlencode

        return f"{base}?{urlencode(qs)}"

    def _fetch_competition_catalog(
        self, competition: str, score: int, season: Optional[int] = None
    ) -> Dict[str, Any]:
        url = self._catalog_url_for(competition, score, season)
        data = self.fetch(url) or {}
        return (data.get("data") or {}).get("players", {})

    def _now_ts(self) -> int:
        return int(datetime.now(timezone.utc).timestamp())

    def get_player_history(
        self,
        player: Player,
        competition: str = "la-liga",
        score: int = 5,
        seasons: Optional[List[int]] = None,
        include_board_events: bool = False,
    ) -> Dict[str, List[Tuple[int, Any]]]:
        """
        Devuelve series históricas aproximadas para un jugador:
          - points: lista de (timestamp|jornada_index, value)
          - price: lista de (timestamp, price)
        Nota: price requiere snapshots persistidos para historia real; si no existen,
        solo devuelve el snapshot actual. points recientes se infieren de fitness.
        """
        history: Dict[str, List[Tuple[int, Any]]] = {"points": [], "price": []}

        cat_now = self._fetch_competition_catalog(competition, score, season=None)
        raw = cat_now.get(str(player.id))
        ts_now = self._now_ts()
        if raw:
            if "price" in raw:
                history["price"].append((ts_now, raw["price"]))

            fitness = raw.get("fitness") or []
            for idx, v in enumerate(fitness):
                if isinstance(v, (int, float)) and v is not None:
                    history["points"].append((idx, v))
            if "pointsLastSeason" in raw and raw["pointsLastSeason"] is not None:
                history["points"].append(
                    (-9999, {"points_last_season": raw["pointsLastSeason"]})
                )

        if seasons:
            for season in seasons:
                cat_season = self._fetch_competition_catalog(
                    competition, score, season=season
                )
                r = cat_season.get(str(player.id))
                if not r:
                    continue
                if "points" in r and r["points"] is not None:
                    history["points"].append((season, {"points_total": r["points"]}))
                if "pointsLastSeason" in r and r["pointsLastSeason"] is not None:
                    history["points"].append(
                        (season - 1, {"points_total": r["pointsLastSeason"]})
                    )
                if "price" in r and r["price"] is not None:
                    history["price"].append((season, r["price"]))

        if include_board_events:
            board_url = (
                url_league + f"{self.account.leagues.id}/board?type=transfer,market"
            )
            board = self.fetch(board_url) or {}
            events = (board.get("data") or {}).get("events", []) or (
                board.get("data") or {}
            ).get("board", [])
            for ev in events:
                ev_player = (
                    (ev.get("player") or {}).get("id")
                    if isinstance(ev.get("player"), dict)
                    else ev.get("player")
                )
                if ev_player == player.id:
                    tstamp = (
                        ev.get("date")
                        or ev.get("ts")
                        or ev.get("time")
                        or self._now_ts()
                    )
                    history["price"].append(
                        (int(tstamp), {"event": ev.get("type", "board")})
                    )

        history["points"].sort(key=lambda x: x)
        history["price"].sort(
            key=lambda x: (isinstance(x, int), x if isinstance(x, int) else 0)
        )
        return history

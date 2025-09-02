"""Library to interact with the Biwenger API."""

import os
import typing as t

from pybiwenger.src.biwenger.league import LeagueAPI
from pybiwenger.src.biwenger.market import MarketAPI
from pybiwenger.src.biwenger.players import PlayersAPI
from pybiwenger.src.client.client import BiwengerBaseClient
from pybiwenger.types.account import *
from pybiwenger.types.account import (AccountData, AccountModel, CurrentUser,
                                      Device, League, LeagueSettings, Location,
                                      UpgradePlan, Upgrades, UserStatus)
from pybiwenger.types.player import Player, players_to_polars
from pybiwenger.types.user import Standing, User
from pybiwenger.utils.log import PabLog

lg = PabLog(__name__)


def authenticate(
    username: t.Optional[str] = None, password: t.Optional[str] = None
) -> None:
    if not username or not password:
        if os.getenv("BIWENGER_USERNAME") and os.getenv("BIWENGER_PASSWORD"):
            lg.log.info("Using existing environment variables for authentication.")
            return
    """Create a Biwenger client instance and log in."""
    os.environ["BIWENGER_USERNAME"] = username
    os.environ["BIWENGER_PASSWORD"] = password
    lg.log.info("Authentication details set in environment variables.")

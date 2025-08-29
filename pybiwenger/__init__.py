"""Library to interact with the Biwenger API."""

import os

from pybiwenger.src.biwenger.market import Market
from pybiwenger.src.biwenger.players import Players
from pybiwenger.src.client.client import BiwengerBaseClient
from pybiwenger.utils.log import PabLog

lg = PabLog(__name__)


def authenticate(username: str, password: str) -> None:
    """Create a Biwenger client instance and log in."""
    os.environ["BIWENGER_USERNAME"] = username
    os.environ["BIWENGER_PASSWORD"] = password
    lg.log.info("Authentication details set in environment variables.")

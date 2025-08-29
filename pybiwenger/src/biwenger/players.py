from pybiwenger.src.client import BiwengerBaseClient
from pydantic import BaseModel
from pybiwenger.utils.log import PabLog
from pybiwenger.src.client.urls import url_all_players

class Player(BaseModel):
    pass

class Players(BiwengerBaseClient):
    def __init__(self) -> None:
        super().__init__()
        self.url = url_all_players
        self.players = self.get_all_players()
        
    def get_all_players(self) -> dict:
        data = self.fetch(self.url)
        return data
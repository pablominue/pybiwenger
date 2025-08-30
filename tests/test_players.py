from pybiwenger.src.biwenger.players import PlayersAPI, Player
from tests.data import PLAYERS

players = [
    Player(player)
    for player in PLAYERS
]

print(players)
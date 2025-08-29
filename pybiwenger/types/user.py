import typing as t

from pydantic import BaseModel

from pybiwenger.types.player import Player


class User(BaseModel):
    id: int
    name: str
    icon: str

    def __str__(self) -> str:
        return self.name

    def __hash__(self) -> t.Any:
        return self.id


class Team(BaseModel):
    owner: User
    players: t.List[Player]

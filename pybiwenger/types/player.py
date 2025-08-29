import typing as t

from pydantic import BaseModel


class Player(BaseModel):
    id: int
    name: str
    slug: str
    team_id: int
    position: int
    price: float
    fantasy_price: float
    status: t.Optional[str]
    price_increment: float
    status_info: t.Optional[str]
    played_home: int
    played_away: int
    fitness: list[float]
    points: int
    points_home: float
    points_away: float
    points_last_season: int

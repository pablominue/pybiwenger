import typing as t

from pydantic import BaseModel, Field


class Player(BaseModel):
    id: int
    name: str
    slug: str
    team_id: t.Optional[int] = Field(alias="teamID", default=0)
    position: int
    price: float
    fantasy_price: float = Field(alias="fantasyPrice", default=0)
    status: t.Optional[str] = None
    price_increment: float = Field(alias="priceIncrement", default=0)
    icon_hero: t.Optional[str] = Field(alias="iconHero", default=None)
    status_info: t.Optional[str] = Field(alias="statusInfo", default=None)
    played_home: int = Field(alias="playedHome", default=0)
    played_away: int = Field(alias="playedAway", default=0)
    fitness: list[t.Optional[t.Union[str, float]]]
    points: int
    points_home: float = Field(alias="pointsHome", default=0)
    points_away: float = Field(alias="pointsAway", default=0)
    points_last_season: t.Optional[int] = Field(alias="pointsLastSeason", default=0)

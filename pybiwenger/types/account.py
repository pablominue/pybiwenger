from typing import Any, List, Optional

from pydantic import BaseModel

from pybiwenger.types.user import User


class Device(BaseModel):
    type: str
    token: str
    updated: int


class AccountModel(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str]
    locale: str
    birthday: int
    status: str
    credits: int
    created: int
    newsletter: bool
    unreadMessages: bool
    lastAccess: int
    source: Optional[str]
    devices: List[Device]


class UserStatus(BaseModel):
    offers: int
    bids: int


class CurrentUser(BaseModel):
    id: int
    name: str
    balance: int
    icon: str
    role: str
    type: str
    joinDate: int
    status: UserStatus
    favorites: List[Any]
    points: int
    position: int

    def to_user(self) -> User:
        return User(id=self.id, name=self.name, icon=self.icon)


class LeagueSettings(BaseModel):
    secret: str
    privacy: str
    onlyAdminPosts: bool
    clause: str
    clauseIncrement: int
    immediateSales: int
    balance: str
    userOffers: str
    loans: str
    loansMinRounds: int
    loansMaxRounds: int
    maxPurchasePrice: int
    challengesAllow: bool
    roundDelayed: str
    marketShowBids: bool
    lineupMultiPos: bool
    lineupAllowExtra: bool
    lineupCoach: bool
    lineupCaptain: bool
    lineupStriker: bool
    lineupReserves: bool
    lineupMaxClubPlayers: bool
    favoritesAllow: bool
    auctions: bool
    customScore: bool


class UpgradePlan(BaseModel):
    id: str
    currency: str
    price: float
    google: str
    huawei: str
    apple: str


class Upgrades(BaseModel):
    premium: UpgradePlan
    ultra: UpgradePlan


class League(BaseModel):
    id: int
    name: str
    competition: str
    scoreID: int
    type: str
    mode: str
    marketMode: str
    created: int
    icon: str
    cover: str
    user: CurrentUser
    settings: LeagueSettings
    upgrades: Upgrades


class Location(BaseModel):
    country: str
    region: str
    city: str


class AccountData(BaseModel):
    account: AccountModel
    leagues: List[League]
    notifications: List[Any]
    location: Location
    lastOfficialLeagueChange: int
    version: int

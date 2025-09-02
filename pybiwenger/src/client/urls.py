"""
The following module contains the utilized URLs for the API classes
"""

url_login = "https://biwenger.as.com/api/v2/auth/login"
url_account = "https://biwenger.as.com/api/v2/account"
url_players_market = "https://biwenger.as.com/api/v2/user?fields=players(id,owner),market(*,-userID),-trophies"
url_players_league = "https://biwenger.as.com/api/v2/players/la-liga"
url_retire_market = "https://biwenger.as.com/api/v2/market?player="
url_user_players = "https://biwenger.as.com/api/v2/user?fields=players(id,owner)"
url_add_player_market = "https://biwenger.as.com/api/v2/market"
url_catalog = "https://biwenger.as.com/api/v2/competitions/la-liga/data?lang=es&score=5"
url_all_players = (
    "https://biwenger.as.com/api/v2/competitions/la-liga/data?lang=es&score=5"
)
url_ranking = "https://biwenger.as.com/api/v2/rounds/league"
url_transfers = (
    "https://biwenger.as.com/api/v2/league/742220/board?type=transfer,market"
)
url_league = ("https://biwenger.as.com/api/v2/league/",)
url_rounds = "https://biwenger.as.com/api/v2/rounds/league"
url_competitions = "https://biwenger.as.com/api/v2/competitions"
url_user = "https://biwenger.as.com/api/v2/user"

url_price_history = "https://cf.biwenger.com/api/v2/players/la-liga/{player_slug}?lang=es&season={yyyy}&fields=*%2Cprices"
url_points_history = "https://cf.biwenger.com/api/v2/players/la-liga/{player_slug}?lang=es&season={yyyy}&fields=*%2Creports(points%2Chome%2Cevents%2Cstatus(status%2CstatusInfo)%2Cmatch(*%2Cround%2Chome%2Caway)"
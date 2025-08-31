# pybiwenger

![pybiwenger logo](https://github.com/pablominue/pybiwenger/blob/main/logo.jpg?raw=true)

**pybiwenger** is a Python library for interacting with the [Biwenger](https://biwenger.as.com/) Soccer Fantasy Game API. It provides convenient access to your account, league, market, and player data, enabling automation and analysis for Biwenger users.

---

## Features

- **Authentication**: Secure login using your Biwenger credentials.
- **Account Management**: Access your user, team, and league information.
- **Players API**: Retrieve player data, rosters, and historical stats.
- **Market API**: Get current market data for players.
- **League API**: Fetch league users and standings.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/pablominue/pybiwenger.git
cd pybiwenger
pip install .
```

Or install via pip:

```bash
pip install pybiwenger
```

---

## Authentication

Before using any API, authenticate with your Biwenger credentials:

```python
import pybiwenger

pybiwenger.authenticate(
    username="your_biwenger_email",
    password="your_biwenger_password"
)
```

Your credentials are stored securely in your local environment variables.

---

## Quickstart Example

```python
from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.src.biwenger.players import PlayersAPI
from pybiwenger.src.biwenger.market import MarketAPI
from pybiwenger.src.biwenger.league import LeagueAPI

# Authenticate first (see above)

# Access account info
client = BiwengerBaseClient()
print("Your team:", client.user_team)

# Get all players in the league
players_api = PlayersAPI()
all_players = players_api.get_all_players()
print("Total players:", len(all_players))

# Get your roster
my_team = players_api.get_user_roster(client.user.id)
print("My roster:", my_team.players)

# Get market data
market_api = MarketAPI()
market = market_api.get_market_data()
print("Market players:", market)

# Get league users and standings
league_api = LeagueAPI()
users = league_api.get_users()
standings = league_api.get_classification()
print("League standings:")
for standing in standings:
    print(f"{standing.position}. {standing.name} - {standing.points} pts")
```

---

## API Reference

### `pybiwenger.src.client.BiwengerBaseClient`

- Handles authentication, session management, and basic API requests.
- Properties:
  - `user_league`: Your league info.
  - `user`: Your user info.
  - `user_team`: Your team (owner + players).
- Methods:
  - `fetch(url: str)`: Fetch data from Biwenger API.

### `pybiwenger.src.biwenger.players.PlayersAPI`

- Inherits from `BiwengerBaseClient`.
- Methods:
  - `get_all_players()`: Returns all players in the competition.
  - `get_league_users()`: Returns all users in your league.
  - `get_user_roster(owner_id: int)`: Returns a user's team.
  - `get_rosters_by_owner()`: Returns all teams in the league.
  - `get_player_history(player, ...)`: Returns historical points and price for a player.

### `pybiwenger.src.biwenger.market.MarketAPI`

- Inherits from `BiwengerBaseClient`.
- Methods:
  - `get_market_data()`: Returns current market data for players.

### `pybiwenger.src.biwenger.league.LeagueAPI`

- Inherits from `BiwengerBaseClient`.
- Methods:
  - `get_users()`: Returns all users in the league.
  - `get_classification()`: Returns current league standings.

---

## Contributing

Pull requests and issues are welcome! Please open an issue for bugs or feature requests.

---

## License

MIT License. See [LICENSE](LICENSE) for details.

---

## Disclaimer

This library is not affiliated with Biwenger or its parent companies. Use at your own risk and respect Biwenger's terms of
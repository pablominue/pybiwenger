import os

from pybiwenger.src.biwenger.market import MarketAPI
from pybiwenger.src.biwenger.players import PlayersAPI
from pybiwenger.src.client import BiwengerBaseClient
from pybiwenger.utils.log import PabLog
from pybiwenger.utils.parsing import Parsing

lg = PabLog(__name__)


class Endpoints:

    # os.environ["BIWENGER_PROXY"] = "" #Include the proxy URL if you want to use one

    @staticmethod
    def daily_squad_market_endpoint(league_name: str = "SIMPS"):

        lg.log.info("Starting daily squad market data extraction...")

        os.environ["BIWENGER_LEAGUE"] = league_name

        client = BiwengerBaseClient()

        league_info = [
            x for x in client.account.leagues if x.name == os.getenv("BIWENGER_LEAGUE")
        ][0]

        user_balance = league_info.user.balance

        lg.log.info(f"User balance: {user_balance}")

        players_api = PlayersAPI()

        roster = players_api.get_user_roster(client.user.id)
        roster_players = roster.players

        market_players = players_api.get_free_players_in_market_data()

        daily_squad_market_data = []

        def get_and_enrich_players_data(players, roster):
            for player in players:
                points_history = players_api.get_points_history_for_inference(
                    player, "2026"
                )
                enriched_info = (
                    Parsing.enrich_and_parse_points_history_info_for_inference(
                        points_history, player, "2026"
                    )
                )
                renamed_enriched_info = (
                    Parsing.rename_points_history_dict_for_inference(
                        enriched_info, roster=roster
                    )
                )
                daily_squad_market_data.append(renamed_enriched_info)

        get_and_enrich_players_data(roster_players, roster=True)
        get_and_enrich_players_data(market_players, roster=False)

        lg.log.info("Finished daily squad market data extraction...")

        return daily_squad_market_data, user_balance

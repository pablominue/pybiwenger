from typing import Any, Dict, List

from pybiwenger.types.player import Player


class Parsing:

    @staticmethod
    def extract_and_flatten_dict(
        data: List[Dict[str, Any]], paths: List[str], delimiter: str = "."
    ) -> List[Dict[str, Any]]:
        """
        Extract specified paths from a list of nested dictionaries and return a flat list of dictionaries.

        :param data: List of dictionaries (can have nested dictionaries)
        :param paths: List of paths to extract, e.g., ["a.b", "c"]
        :param delimiter: Delimiter used in paths to indicate nesting
        :return: Flat list of dictionaries with string keys and string values
        """

        def get_nested_value(d: Dict[str, Any], path: List[str]):
            """Recursively get the nested value from a dictionary, or None if not present."""
            current = d
            for key in path:
                if isinstance(current, dict) and key in current:
                    current = current[key]
                else:
                    return None
            return current

        flat_list = []
        for item in data:
            flat_item = {}
            for path in paths:
                keys = path.split(delimiter)
                value = get_nested_value(item, keys)
                if value is not None:
                    flat_item[path] = value
            if flat_item:
                flat_list.append(flat_item)

        return flat_list

    @staticmethod
    def enrich_and_parse_points_history_info(
        data: List[Dict[str, Any]], player: Player, year: str
    ) -> List[Dict[str, str]]:

        def count_event_types(data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
            # The event types we're interested in
            target_types = {1, 2, 3, 7, 8}

            for item in data:
                events = item.get("events", [])

                # Initialize counts
                counts = {f"event_type_{t}": 0 for t in target_types}

                # Count events
                for ev in events:
                    t = ev.get("type")
                    if t in target_types:
                        counts[f"event_type_{t}"] += 1

                # Add counts to the parent dict
                item.update(counts)

            return data

        season = {"season": year}

        player_flatted_info = player.model_dump(include={"slug", "position"})
        for d in data:
            d.update(player_flatted_info)
            d.update(season)

        data = count_event_types(data)

        for d in data:
            d.pop("events", None)

        return data

    @staticmethod
    def enrich_and_parse_points_history_info_for_inference(
        data: List[Dict[str, Any]], player: Player, year: str
    ) -> List[Dict[str, str]]:

        season = {"season": year}

        player_flatted_info = player.model_dump(
            include={"slug", "position", "status", "status_info", "price"}
        )
        for d in data:
            d.update(player_flatted_info)
            d.update(season)

        for d in data:
            d.pop("events", None)

        return data

    @staticmethod
    def rename_points_history_dict(data: List[Dict[str, str]]) -> List[Dict[str, str]]:
        mapping = {
            "status.status": "status",
            "match.home.slug": "home_team",
            "match.away.slug": "away_team",
            "match.date": "date",
            "rawStats.roundPhase": "league_round",
            "rawStats.homeScore": "home_team_goals",
            "rawStats.awayScore": "away_team_goals",
            "rawStats.picas": "picas_as",
            "rawStats.sofascore": "sofascore_score",
            "rawStats.score5": "puntuacion_media_sofascore_as",
            "slug": "player",
            "event_type_1": "player_non_penalti_goals",
            "event_type_2": "player_penalti_goals",
            "event_type_3": "player_assists",
            "event_type_7": "player_red_card",
            "event_type_8": "player_second_yellow",
            "position": "player_position",
            "home": "is_player_home",
            "rawStats.price": "player_price",
            "rawStats.minutesPlayed": "minutes_played",
        }

        for d in data:
            for old_key, new_key in mapping.items():
                if old_key in d:
                    d[new_key] = d.pop(old_key)

        return data

    def rename_points_history_dict_for_inference(
        data: List[Dict[str, str]], roster
    ) -> List[Dict[str, str]]:
        mapping = {
            "status": "status",
            "status_info": "status_info",
            "match.home.slug": "home_team",
            "match.away.slug": "away_team",
            "match.date": "date",
            "rawStats.roundPhase": "league_round",
            "rawStats.score5": "puntuacion_media_sofascore_as",
            "slug": "player",
            "position": "player_position",
            "home": "is_player_home",
            "rawStats.price": "player_price_for_match",
            "price": "player_price_now",
            "rawStats.minutesPlayed": "minutes_played",
            "season": "season",
        }

        for d in data:
            for old_key, new_key in mapping.items():
                if old_key in d:
                    d[new_key] = d.pop(old_key)
            if roster:
                d["roster"] = True
            elif roster == False:
                d["roster"] = False

        return data

    @staticmethod
    def reformat_market_history(data: List[List[str]]) -> List[Dict[str, str]]:

        result = [{"date_yyMMdd": d[0], "price": d[1]} for d in data]

        return result

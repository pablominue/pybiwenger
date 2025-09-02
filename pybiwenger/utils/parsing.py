from typing import (Any, Dict, List)

class Parsing:

    @staticmethod
    def extract_info(data: List[Dict[str, Any]], paths: List[str], delimiter: str = '.') -> List[Dict[str, str]]:
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
                    flat_item[path] = str(value)
            if flat_item:
                flat_list.append(flat_item)

        return flat_list
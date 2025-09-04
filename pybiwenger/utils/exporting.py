import csv
from typing import Any, Dict, List


class Exporting:

    @staticmethod
    def exporting_list_dicts_to_csv(data: List[Dict[str, str]], path: str):
        # Determine fieldnames (keys). Assumes all dicts share the same set of keys or a superset.
        fieldnames = set()
        for item in data:
            fieldnames.update(item.keys())
        fieldnames = list(fieldnames)

        # Write CSV
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

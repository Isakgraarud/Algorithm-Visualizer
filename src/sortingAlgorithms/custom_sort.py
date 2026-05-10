from src.sort_step import SortStep


class CustomSort:
    """Placeholder for a user-defined sorting algorithm."""

    PSEUDOCODE = [
        "# Write your algorithm here",
        "# yield SortStep(data, ...) each step",
    ]

    COMPLEXITY = {
        "best":    "N/A",
        "average": "N/A",
        "worst":   "N/A",
        "space":   "N/A",
    }

    @staticmethod
    def run(data):
        yield SortStep(data=data, log="Custom Sort: add your logic in custom_sort.py")

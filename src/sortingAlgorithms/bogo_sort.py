import random
from src.sort_step import SortStep
from src import constants as c


class BogoSort:
    """
    Bogosort randomly shuffles until the array is sorted.

    Complexity:
    - Best Case:  O(n)      (already sorted)
    - Average:    O(n·n!)
    - Worst Case: Unbounded
    - Space:      O(1)

    (@link https://en.wikipedia.org/wiki/Bogosort 08.05.2026)
    """

    PSEUDOCODE = [
        "while not is_sorted(data):",
        "  shuffle(data)",
        "def is_sorted(data):",
        "  for i in range(n-1):",
        "    if data[i] > data[i+1]: return False",
        "  return True",
    ]

    COMPLEXITY = {
        "best":    "O(n)",
        "average": "O(n·n!)",
        "worst":   "Unbounded",
        "space":   "O(1)",
    }

    @staticmethod
    def run(data):
        def is_sorted(arr):
            return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

        attempts = 0
        while not is_sorted(data):
            random.shuffle(data)
            attempts += 1
            rng = random.randint(0, len(data) - 1)
            yield SortStep(
                data=data,
                color_map={rng: c.ROLE_COMPARING},
                variables={"attempts": attempts},
                pseudocode_line=1,
                log=f"Shuffle #{attempts} — still not sorted",
                comparisons_delta=len(data) - 1,
            )

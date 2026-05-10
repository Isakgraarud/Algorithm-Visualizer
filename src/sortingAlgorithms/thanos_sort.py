import random
from src.sort_step import SortStep
from src import constants as c


class ThanosSort:
    """
    Thanos Sort snaps half the elements out of existence until the remainder is sorted.
    Perfectly balanced, as all things should be.

    Complexity:
    - Best Case:  O(n)          (already sorted)
    - Average:    O(n log n)    snaps to reach a sorted state
    - Worst Case: O(n)          reduces to one element
    - Space:      O(1)

    (@link https://github.com/gustavo-depaula/stalin-sort 08.05.2026)
    """

    PSEUDOCODE = [
        "while not is_sorted(data):",
        "  keep = random_half(indices)",
        "  data = [data[i] for i in keep]",
        "  # half the elements are gone",
    ]

    COMPLEXITY = {
        "best":    "O(n)",
        "average": "O(n log n)",
        "worst":   "O(n)",
        "space":   "O(1)",
    }

    @staticmethod
    def run(data):
        def is_sorted(arr):
            return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

        snap = 0
        yield SortStep(
            data=data,
            pseudocode_line=0,
            log="Thanos has arrived. He will snap until balance is achieved.",
        )
        while not is_sorted(data) and len(data) > 1:
            snap += 1
            before = len(data)
            survivors = sorted(random.sample(range(len(data)), len(data) // 2))
            kept = [data[i] for i in survivors]
            data.clear()
            data.extend(kept)
            yield SortStep(
                data=data,
                color_map={i: c.ROLE_SORTED for i in range(len(data))},
                variables={"snap": snap, "remaining": len(data), "removed": before - len(data)},
                pseudocode_line=2,
                log=f"Snap #{snap}: {before - len(data)} elements eliminated, {len(data)} remain",
                comparisons_delta=before - 1,
            )

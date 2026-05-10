from src.sort_step import SortStep
from src import constants as c


class BubbleSort:
    """
    Bubble Sort repeatedly compares adjacent elements and swaps them if out of order.
    After each pass the largest unsorted element bubbles to its final position.

    Complexity:
    - Best Case:    O(n)   (already sorted — early exit)
    - Average Case: O(n²)
    - Worst Case:   O(n²)
    - Space:        O(1)

    (@link https://en.wikipedia.org/wiki/Bubble_sort 08.05.2026)
    """

    PSEUDOCODE = [
        "for i in range(n):",
        "  swapped = False",
        "  for j in range(n - i - 1):",
        "    if data[j] > data[j+1]:",
        "      swap(data[j], data[j+1])",
        "      swapped = True",
        "  if not swapped: break",
    ]

    COMPLEXITY = {
        "best":    "O(n)",
        "average": "O(n²)",
        "worst":   "O(n²)",
        "space":   "O(1)",
    }

    @staticmethod
    def run(data):
        n = len(data)
        sorted_set: set = set()
        for i in range(n):
            swapped = False
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                variables={"i": i, "n": n},
                pseudocode_line=0,
                log=f"Pass {i + 1} of {n}",
            )
            for j in range(0, n - i - 1):
                yield SortStep(
                    data=data, sorted_set=set(sorted_set),
                    color_map={j: c.ROLE_COMPARING, j + 1: c.ROLE_COMPARING},
                    variables={"i": i, "j": j},
                    pseudocode_line=3,
                    log=f"Compare data[{j}]={data[j]} and data[{j+1}]={data[j+1]}",
                    comparisons_delta=1,
                )
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    swapped = True
                    yield SortStep(
                        data=data, sorted_set=set(sorted_set),
                        color_map={j: c.ROLE_SWAP, j + 1: c.ROLE_SWAP},
                        variables={"i": i, "j": j},
                        pseudocode_line=4,
                        log=f"Swapped index {j} and {j + 1}",
                        swaps_delta=1,
                    )
            sorted_set.add(n - i - 1)
            if not swapped:
                yield SortStep(
                    data=data, sorted_set=set(sorted_set),
                    variables={"i": i},
                    pseudocode_line=6,
                    log="No swaps this pass — array is sorted, stopping early",
                )
                break

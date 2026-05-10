from src.sort_step import SortStep
from src import constants as c


class QuickSort:
    PSEUDOCODE = [
        "def partition(data, low, high):",
        "  pivot = data[high]",
        "  i = low - 1",
        "  for j in range(low, high):",
        "    if data[j] <= pivot:",
        "      i += 1",
        "      swap(data[i], data[j])",
        "  swap(data[i+1], data[high])",
        "  return i + 1",
        "def quicksort(data, low, high):",
        "  if low < high:",
        "    pi = partition(data, low, high)",
        "    quicksort(data, low, pi-1)",
        "    quicksort(data, pi+1, high)",
    ]

    COMPLEXITY = {
        "best":    "O(n log n)",
        "average": "O(n log n)",
        "worst":   "O(n²)",
        "space":   "O(log n)",
    }

    @staticmethod
    def run(data):
        sorted_set: set = set()
        yield from QuickSort._quicksort(data, 0, len(data) - 1, sorted_set)

    @staticmethod
    def _quicksort(data, low, high, sorted_set):
        if low < high:
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                color_map={low: c.ROLE_COMPARING, high: c.ROLE_COMPARING},
                variables={"low": low, "high": high},
                pseudocode_line=10,
                log=f"quicksort(low={low}, high={high})",
            )
            pi_gen = QuickSort._partition(data, low, high, sorted_set)
            pi = None
            for step in pi_gen:
                if isinstance(step, int):
                    pi = step
                else:
                    yield step
            if pi is not None:
                sorted_set.add(pi)
                yield from QuickSort._quicksort(data, low, pi - 1, sorted_set)
                yield from QuickSort._quicksort(data, pi + 1, high, sorted_set)

    @staticmethod
    def _partition(data, low, high, sorted_set):
        pivot = data[high]
        i = low - 1
        yield SortStep(
            data=data, sorted_set=set(sorted_set),
            color_map={high: c.ROLE_PIVOT},
            variables={"low": low, "high": high, "pivot": pivot, "i": i},
            pseudocode_line=1,
            log=f"Pivot = {pivot} (index {high})",
        )
        for j in range(low, high):
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                color_map={j: c.ROLE_COMPARING, high: c.ROLE_PIVOT, i: c.ROLE_MIN} if i >= low else {j: c.ROLE_COMPARING, high: c.ROLE_PIVOT},
                variables={"low": low, "high": high, "pivot": pivot, "i": i, "j": j},
                pseudocode_line=4,
                log=f"Compare data[{j}]={data[j]} <= pivot={pivot}",
                comparisons_delta=1,
            )
            if data[j] <= pivot:
                i += 1
                data[i], data[j] = data[j], data[i]
                yield SortStep(
                    data=data, sorted_set=set(sorted_set),
                    color_map={i: c.ROLE_SWAP, j: c.ROLE_SWAP, high: c.ROLE_PIVOT},
                    variables={"low": low, "high": high, "pivot": pivot, "i": i, "j": j},
                    pseudocode_line=6,
                    log=f"Swapped index {i} and {j}",
                    swaps_delta=1,
                )
        data[i + 1], data[high] = data[high], data[i + 1]
        yield SortStep(
            data=data, sorted_set=set(sorted_set),
            color_map={i+1: c.ROLE_SORTED, high: c.ROLE_SWAP},
            variables={"low": low, "high": high, "pivot": pivot, "pi": i+1},
            pseudocode_line=7,
            log=f"Pivot placed at index {i+1}",
            swaps_delta=1,
        )
        yield i + 1   # signal the partition index back to _quicksort

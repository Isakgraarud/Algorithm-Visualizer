from src.sort_step import SortStep
from src import constants as c


class SelectionSort:
    PSEUDOCODE = [
        "for i in range(n):",
        "  min_idx = i",
        "  for j in range(i+1, n):",
        "    if data[j] < data[min_idx]:",
        "      min_idx = j",
        "  swap(data[i], data[min_idx])",
    ]

    COMPLEXITY = {
        "best":    "O(n²)",
        "average": "O(n²)",
        "worst":   "O(n²)",
        "space":   "O(1)",
    }

    @staticmethod
    def run(data):
        n = len(data)
        sorted_set = set()
        for i in range(n):
            min_idx = i
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                color_map={i: c.ROLE_MIN},
                variables={"i": i, "min_idx": min_idx, "n": n},
                pseudocode_line=1,
                log=f"Pass {i+1}: searching for minimum starting at index {i}",
            )
            for j in range(i + 1, n):
                yield SortStep(
                    data=data, sorted_set=set(sorted_set),
                    color_map={j: c.ROLE_COMPARING, min_idx: c.ROLE_MIN},
                    variables={"i": i, "j": j, "min_idx": min_idx},
                    pseudocode_line=3,
                    log=f"Comparing data[{j}]={data[j]} < data[{min_idx}]={data[min_idx]}",
                    comparisons_delta=1,
                )
                if data[j] < data[min_idx]:
                    min_idx = j
                    yield SortStep(
                        data=data, sorted_set=set(sorted_set),
                        color_map={min_idx: c.ROLE_MIN},
                        variables={"i": i, "j": j, "min_idx": min_idx},
                        pseudocode_line=4,
                        log=f"New minimum found: data[{min_idx}]={data[min_idx]}",
                    )
            if min_idx != i:
                data[i], data[min_idx] = data[min_idx], data[i]
                yield SortStep(
                    data=data, sorted_set=set(sorted_set),
                    color_map={i: c.ROLE_SWAP, min_idx: c.ROLE_SWAP},
                    variables={"i": i, "min_idx": min_idx},
                    pseudocode_line=5,
                    log=f"Swapped index {i} and {min_idx}",
                    swaps_delta=1,
                )
            sorted_set.add(i)

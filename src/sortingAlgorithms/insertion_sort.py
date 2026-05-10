from src.sort_step import SortStep
from src import constants as c


class InsertionSort:
    PSEUDOCODE = [
        "for i in range(1, n):",
        "  key = data[i]",
        "  j = i - 1",
        "  while j >= 0 and data[j] > key:",
        "    data[j+1] = data[j]",
        "    j -= 1",
        "  data[j+1] = key",
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
        sorted_set = set()
        sorted_set.add(0)
        for i in range(1, n):
            key = data[i]
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                color_map={i: c.ROLE_PIVOT},
                variables={"i": i, "key": key, "n": n},
                pseudocode_line=1,
                log=f"Picked key = {key} at index {i}",
            )
            j = i - 1
            while j >= 0:
                yield SortStep(
                    data=data, sorted_set=set(sorted_set),
                    color_map={j: c.ROLE_COMPARING, i: c.ROLE_PIVOT},
                    variables={"i": i, "j": j, "key": key},
                    pseudocode_line=3,
                    log=f"Comparing data[{j}]={data[j]} > key={key}",
                    comparisons_delta=1,
                )
                if data[j] <= key:
                    break
                data[j + 1] = data[j]
                yield SortStep(
                    data=data, sorted_set=set(sorted_set),
                    color_map={j: c.ROLE_SWAP, j+1: c.ROLE_SWAP},
                    variables={"i": i, "j": j, "key": key},
                    pseudocode_line=4,
                    log=f"Shifted data[{j}]={data[j+1]} right to index {j+1}",
                    swaps_delta=1,
                )
                j -= 1
            data[j + 1] = key
            sorted_set.add(i)
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                color_map={j+1: c.ROLE_SORTED},
                variables={"i": i, "j": j, "key": key},
                pseudocode_line=6,
                log=f"Inserted key={key} at index {j+1}",
            )

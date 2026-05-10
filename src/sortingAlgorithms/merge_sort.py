from src.sort_step import SortStep
from src import constants as c


class MergeSort:
    PSEUDOCODE = [
        "def merge_sort(data, left, right):",
        "  if left >= right: return",
        "  mid = (left + right) // 2",
        "  merge_sort(data, left, mid)",
        "  merge_sort(data, mid+1, right)",
        "  merge(data, left, mid, right)",
        "def merge(data, left, mid, right):",
        "  L = data[left:mid+1]",
        "  R = data[mid+1:right+1]",
        "  i = j = 0; k = left",
        "  while i < len(L) and j < len(R):",
        "    if L[i] <= R[j]: data[k]=L[i]; i+=1",
        "    else:             data[k]=R[j]; j+=1",
        "    k += 1",
        "  copy remaining L or R",
    ]

    COMPLEXITY = {
        "best":    "O(n log n)",
        "average": "O(n log n)",
        "worst":   "O(n log n)",
        "space":   "O(n)",
    }

    @staticmethod
    def run(data):
        sorted_set: set = set()
        yield from MergeSort._merge_sort(data, 0, len(data) - 1, sorted_set)
        # Mark all sorted at end
        sorted_set.update(range(len(data)))

    @staticmethod
    def _merge_sort(data, left, right, sorted_set):
        if left >= right:
            sorted_set.add(left)
            return
        mid = (left + right) // 2
        yield SortStep(
            data=data, sorted_set=set(sorted_set),
            color_map={i: c.ROLE_COMPARING for i in range(left, right + 1)},
            variables={"left": left, "right": right, "mid": mid},
            pseudocode_line=2,
            log=f"Splitting [{left}..{right}] at mid={mid}",
        )
        yield from MergeSort._merge_sort(data, left, mid, sorted_set)
        yield from MergeSort._merge_sort(data, mid + 1, right, sorted_set)
        yield from MergeSort._merge(data, left, mid, right, sorted_set)

    @staticmethod
    def _merge(data, left, mid, right, sorted_set):
        L = data[left:mid + 1]
        R = data[mid + 1:right + 1]
        i = j = 0
        k = left
        yield SortStep(
            data=data, sorted_set=set(sorted_set),
            color_map={x: c.ROLE_COMPARING for x in range(left, right + 1)},
            variables={"left": left, "mid": mid, "right": right, "k": k},
            pseudocode_line=6,
            log=f"Merging [{left}..{mid}] and [{mid+1}..{right}]",
        )
        while i < len(L) and j < len(R):
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                color_map={left + i: c.ROLE_COMPARING, mid + 1 + j: c.ROLE_COMPARING, k: c.ROLE_PIVOT},
                variables={"i": i, "j": j, "k": k, "L[i]": L[i], "R[j]": R[j]},
                pseudocode_line=10,
                log=f"Compare L[{i}]={L[i]} and R[{j}]={R[j]}",
                comparisons_delta=1,
            )
            if L[i] <= R[j]:
                data[k] = L[i]
                i += 1
            else:
                data[k] = R[j]
                j += 1
            sorted_set.add(k)
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                color_map={k: c.ROLE_SORTED},
                variables={"i": i, "j": j, "k": k},
                pseudocode_line=11,
                log=f"Placed {data[k]} at index {k}",
                swaps_delta=1,
            )
            k += 1
        while i < len(L):
            data[k] = L[i]
            sorted_set.add(k)
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                color_map={k: c.ROLE_SORTED},
                variables={"k": k, "value": L[i]},
                pseudocode_line=14,
                log=f"Copying remaining L[{i}]={L[i]} to index {k}",
            )
            i += 1
            k += 1
        while j < len(R):
            data[k] = R[j]
            sorted_set.add(k)
            yield SortStep(
                data=data, sorted_set=set(sorted_set),
                color_map={k: c.ROLE_SORTED},
                variables={"k": k, "value": R[j]},
                pseudocode_line=14,
                log=f"Copying remaining R[{j}]={R[j]} to index {k}",
            )
            j += 1
            k += 1

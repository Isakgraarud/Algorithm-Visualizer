from src.sort_step import SortStep
from src import constants as c


class StalinSort:
    """
    Stalin Sort removes any element smaller than the previous one.
    The result is a sorted subsequence — the non-conforming elements are purged.

    Complexity: O(n) — a single destructive pass.

    (@link https://github.com/gustavo-depaula/stalin-sort 08.05.2026)
    """

    PSEUDOCODE = [
        "result = [data[0]]",
        "for each element e in data[1:]:",
        "  if e >= result.last:",
        "    result.append(e)",
        "  else:",
        "    remove(e)  # send to gulag",
    ]

    COMPLEXITY = {
        "best":    "O(n)",
        "average": "O(n)",
        "worst":   "O(n)",
        "space":   "O(1)",
    }

    @staticmethod
    def run(data):
        yield SortStep(
            data=data,
            pseudocode_line=0,
            log="Stalin Sort: non-conforming elements will be purged",
        )
        i = 1
        purged = 0
        while i < len(data):
            yield SortStep(
                data=data,
                color_map={i: c.ROLE_COMPARING, i - 1: c.ROLE_MIN},
                variables={"i": i, "purged": purged},
                pseudocode_line=2,
                log=f"Inspect data[{i}]={data[i]} vs data[{i-1}]={data[i-1]}",
                comparisons_delta=1,
            )
            if data[i] < data[i - 1]:
                val = data[i]
                del data[i]
                purged += 1
                highlight = i - 1 if i - 1 < len(data) else len(data) - 1
                yield SortStep(
                    data=data,
                    color_map={highlight: c.ROLE_COMPARING} if highlight >= 0 else {},
                    variables={"i": i, "purged": purged},
                    pseudocode_line=5,
                    log=f"Purged {val} — does not conform",
                )
            else:
                yield SortStep(
                    data=data,
                    color_map={i: c.ROLE_SORTED, i - 1: c.ROLE_SORTED},
                    variables={"i": i, "purged": purged},
                    pseudocode_line=3,
                    log=f"data[{i}]={data[i]} conforms — kept",
                )
                i += 1

import threading
import time
import queue

from src.sort_step import SortStep
from src import constants as c


class SleepSort:
    """
    Each element spawns a thread that sleeps proportional to its value.
    Threads wake up in order, naturally producing a sorted sequence.

    Complexity:
    - Time:  O(max(arr) + n) — dominated by the largest element's sleep
    - Space: O(n)            — one thread per element

    (@link https://en.wikipedia.org/wiki/Sleep_sort)
    """

    PSEUDOCODE = [
        "for each element e in data:",
        "  spawn thread: sleep(e/scale), emit e",
        "start all threads",
        "sorted = []",
        "while len(sorted) < n:",
        "  e = queue.get()",
        "  sorted.append(e)",
    ]

    COMPLEXITY = {
        "best":    "O(n + max)",
        "average": "O(n + max)",
        "worst":   "O(n + max)",
        "space":   "O(n)",
    }

    @staticmethod
    def run(data):
        if not data:
            return

        result_queue: queue.Queue = queue.Queue()
        original = list(data)
        scale = max(c.MIN_VAL, 1)

        def worker(num):
            time.sleep(num / scale * 0.15)
            result_queue.put(num)

        threads = [threading.Thread(target=worker, args=(v,), daemon=True) for v in original]
        for t in threads:
            t.start()

        yield SortStep(
            data=data,
            variables={"n": len(original), "threads": len(threads)},
            pseudocode_line=2,
            log=f"Spawned {len(threads)} threads — waiting for them to wake up",
        )

        sorted_values = []
        remaining = list(original)

        while len(sorted_values) < len(original):
            try:
                num = result_queue.get_nowait()
                sorted_values.append(num)
                remaining.remove(num)
                new_data = sorted_values + remaining
                data.clear()
                data.extend(new_data)
                idx = len(sorted_values) - 1
                yield SortStep(
                    data=data,
                    color_map={idx: c.ROLE_SORTED},
                    sorted_set=set(range(len(sorted_values))),
                    variables={"sorted": len(sorted_values), "remaining": len(remaining)},
                    pseudocode_line=6,
                    log=f"Thread for value {num} woke up — placed at index {idx}",
                )
            except queue.Empty:
                yield SortStep(
                    data=data,
                    sorted_set=set(range(len(sorted_values))),
                    variables={"sorted": len(sorted_values), "remaining": len(remaining)},
                    pseudocode_line=4,
                )

        for t in threads:
            t.join(timeout=0.1)

import threading
import time
import queue
from ..constants import MIN_VAL

class SleepSort:
    """
    Sleep Sort Implementation

    Sleep Sort is an unconventional, concurrency-based sorting algorithm. For
    each element in the list, a thread is spawned that sleeps for a duration
    proportional to the element's value before "reporting in." Because larger
    values sleep longer, the threads naturally finish in ascending order,
    producing a sorted sequence as a side effect of OS scheduling.

    In this visualization, each thread sleeps for a number of milliseconds
    equal to its bar height — so taller bars literally take longer to wake up.

    Note: This algorithm does NOT work correctly for negative numbers, and its
    accuracy depends on thread scheduling precision.

    Complexity:
    - Time: O(max(arr) + n) - dominated by the largest element's sleep time.
    - Space: O(n) - one thread per element.

    (@link https://en.wikipedia.org/wiki/Sleep_sort)
    """

    @staticmethod
    def run(data):
        if not data:
            return

        result_queue = queue.Queue()
        original = list(data)

        def worker(num):
            time.sleep(num / MIN_VAL)
            result_queue.put(num)

        threads = []
        for num in original:
            t = threading.Thread(target=worker, args=(num,), daemon=True)
            threads.append(t)
            t.start()

        yield data, []

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

                yield data, [len(sorted_values) - 1]
            except queue.Empty:
                yield data, []

        for t in threads:
            t.join(timeout=0.1)
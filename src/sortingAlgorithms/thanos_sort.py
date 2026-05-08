import random

class ThanosSort:
    """
    Thanos Sort Implementation

    Thanos Sort is a humorous, non-functional sorting algorithm inspired by the
    Marvel villain Thanos. If the list is not sorted, it "snaps" — randomly
    eliminating half of the elements — and repeats the process until, by sheer
    luck, the surviving elements happen to be in order.

    Note: This algorithm is destructive. It does NOT sort the original data;
    it produces a sorted subsequence by discarding elements. Perfectly balanced,
    as all things should be.

    Complexity:
    - Best Case: O(n) - The list is already sorted.
    - Average Case: O(n log n) snaps on average before a sorted state remains.
    - Worst Case: Reduces to a single element (always trivially sorted).
    - Space Complexity: O(1) (in-place mutation of the input list).

    (@link https://github.com/gustavo-depaula/stalin-sort Inspired by joke sorts)
    """

    @staticmethod
    def run(data):
        def is_sorted(arr):
            return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

        yield data, []

        while not is_sorted(data) and len(data) > 1:
            survivors = sorted(random.sample(range(len(data)), len(data) // 2))
            snapped = [data[i] for i in survivors]

            data.clear()
            data.extend(snapped)

            yield data, list(range(len(data)))
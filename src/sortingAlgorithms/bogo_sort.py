import random

class BogoSort:

    """
    Bogosort (also known as Monkey Sort, Stupid Sort, or Slowsort) implementation.

    Bogosort is an extremely inefficient, non-functional sorting algorithm based on
    the 'generate and test' paradigm. It works by randomly shuffling an input list,
    checking if it is sorted, and repeating this process until the list is
    miraculously in order.

    Complexity:
    - Best Case: O(n) - The list is already sorted.
    - Average Case: O(n * n!) - For large n, this is computationally unfeasible.
    - Worst Case: Unbounded (Infinite) - It is theoretically possible to never shuffle
      the list into the correct order.
    - Space Complexity: O(1)

    (@link https://en.wikipedia.org/wiki/Bogosort 08.05.2026)
    """

    @staticmethod
    def run(data):
        def is_sorted(arr):
            return all(arr[i] <= arr[i+1] for i in range(len(arr)-1))

        while not is_sorted(data):
            random.shuffle(data)
            yield data, [random.randint(0, len(data)-1)]
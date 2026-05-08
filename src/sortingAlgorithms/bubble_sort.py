class BubbleSort:

    """
    Bubble Sort Implementation

    Bubble Sort is a simple, comparison-based algorithm that sorts a list by
    repeatedly stepping through it, comparing adjacent elements, and swapping
    them if they are in the wrong order.

    Complexity:
    - Best Case: O(n) (when the list is already sorted)
    - Average Case: O(n^2)
    - Worst Case: O(n^2)
    - Space Complexity: O(1)

    (@link https://en.wikipedia.org/wiki/Bubble_sort 08.05.2026)
    """

    @staticmethod
    def run(data):
        n = len(data)
        for i in range(n):
            for j in range(0, n - i - 1):
                if data[j] > data[j + 1]:
                    data[j], data[j + 1] = data[j + 1], data[j]
                    yield data, [j, j + 1]
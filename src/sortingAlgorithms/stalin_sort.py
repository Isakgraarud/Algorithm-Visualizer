class StalinSort:
    """
    Stalin Sort Implementation

    Stalin Sort is a humorous, non-functional sorting algorithm that enforces
    order through elimination. It iterates through the list once and "exiles"
    (removes) any element that is smaller than the previous one. What remains
    is, by definition, a non-decreasing sequence.

    Note: This algorithm is destructive. It does NOT sort the original data;
    it produces a sorted subsequence by discarding any element that dares to
    step out of line.

    Complexity:
    - Best Case: O(n) - The list is already sorted; no elements are removed.
    - Average Case: O(n)
    - Worst Case: O(n) - A single pass is always sufficient.
    - Space Complexity: O(1) (in-place mutation of the input list).

    (@link https://github.com/gustavo-depaula/stalin-sort 08.05.2026)
    """

    @staticmethod
    def run(data):
        yield data, []

        i = 1
        while i < len(data):
            if data[i] < data[i - 1]:
                del data[i]
                yield data, [i - 1] if i - 1 < len(data) else []
            else:
                yield data, [i - 1, i]
                i += 1
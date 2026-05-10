# Algorithm Visualizer

A Python-based sorting algorithm visualizer built with Tkinter.

## Features

- **Live animation** — watch bars being compared, swapped, and sorted in real time
- **Compare mode** — run two algorithms side by side on identical data
- **Step mode** — step forward and backward through every operation
- **Sound** — audio feedback tied to bar height during sorting
- **Pseudocode panel** — highlights the current line of pseudocode as the algorithm runs
- **Variables panel** — shows live algorithm state (indices, pivot, etc.)
- **Complexity panel** — displays time and space complexity for the selected algorithm
- **Stats panel** — tracks comparisons, swaps, and elapsed time
- **Log panel** — records a human-readable trace of operations
- **Data presets** — Random, Sorted, Reversed, Nearly Sorted, Few Unique
- **Adjustable speed and array size**
- **Color-coded bars** — blue (default), coral (comparing), orange (swapping), amber (pivot), violet (minimum), green (sorted)

## Implemented Algorithms

| Algorithm | Category |
|---|---|
| Bubble Sort | Comparison |
| Insertion Sort | Comparison |
| Selection Sort | Comparison |
| Merge Sort | Divide & Conquer |
| Quick Sort | Divide & Conquer |
| Bogo Sort | Joke / Brute-force |
| Stalin Sort | Joke |
| Thanos Sort | Joke |
| Sleep Sort | Joke |
| Custom Sort | Template |

## Requirements

- Python 3.10+
- Tkinter (included with most Python distributions)
- `pygame` (for sound — optional, sound toggle is in the UI)

Install dependencies:

```bash
pip install pygame
```

## Running

```bash
python -m src.main
```

## Adding a New Algorithm

1. Create a `.py` file in `src/sortingAlgorithms/`
2. Define a class with a `run(data)` classmethod that `yield`s `SortStep` objects
3. The visualizer auto-discovers all classes in that folder — no registration needed

Minimal example:

```python
from src.sort_step import SortStep
from src import constants as c

class MySort:
    COMPLEXITY = {
        "Best": "O(n)", "Average": "O(n²)", "Worst": "O(n²)", "Space": "O(1)"
    }
    PSEUDOCODE = [
        "for i in range(n):",
        "    ...",
    ]

    @classmethod
    def run(cls, data):
        data = list(data)
        # ... your sorting logic ...
        yield SortStep(
            data=data,
            color_map={i: c.ROLE_COMPARING, j: c.ROLE_SWAP},
            comparisons_delta=1,
            swaps_delta=1,
            pseudocode_line=0,
            log="Comparing elements",
        )
```

See `src/sort_step.py` for all `SortStep` fields and `src/constants.py` for available color roles.

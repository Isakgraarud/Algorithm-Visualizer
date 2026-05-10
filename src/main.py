import re
import tkinter as tk
import importlib
import inspect
from pathlib import Path

from src.visualizer import SortingVisualizer
from src import constants as c


def get_sorting_algorithms() -> dict:
    algorithms = {}
    path = Path(__file__).parent / "sortingAlgorithms"
    for file in sorted(path.glob("*.py")):
        if file.stem == "__init__":
            continue
        module_name = f"src.sortingAlgorithms.{file.stem}"
        module = importlib.import_module(module_name)
        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module_name:
                display = re.sub(r"(\w)([A-Z])", r"\1 \2", name)
                algorithms[display] = obj
    return algorithms


def main():
    root = tk.Tk()
    root.geometry(f"{c.WINDOW_WIDTH}x{c.WINDOW_HEIGHT}")
    root.resizable(True, True)
    root.minsize(900, 500)

    algorithms = get_sorting_algorithms()
    SortingVisualizer(root, algorithms)
    root.mainloop()


if __name__ == "__main__":
    main()

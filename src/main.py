import tkinter as tk
import importlib
import inspect

from src.visualizer import SortingVisualizer
from pathlib import Path

def getSortingAlgorithms():
    available_algorithms = {}
    path = Path(__file__).parent / "sortingAlgorithms"

    for file in path.glob("*.py"):
        if file.stem == "__init__":
            continue

        moduleName = f"src.sortingAlgorithms.{file.stem}"
        module = importlib.import_module(moduleName)

        for name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == moduleName:
                import re
                display_name = re.sub(r"(\w)([A-Z])", r"\1 \2", name)
                available_algorithms[display_name] = obj

    return available_algorithms

def main():
    root = tk.Tk()

    available_algorithms = getSortingAlgorithms()

    app = SortingVisualizer(root, available_algorithms)
    root.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from visualizer import SortingVisualizer
from src.sortingAlgorithms.bubble_sort import BubbleSort
from src.sortingAlgorithms.bogo_sort import BogoSort

def main():
    root = tk.Tk()

    available_algorithms = {
        "Bubble Sort": BubbleSort,
        "Bogo Sort": BogoSort
    }

    app = SortingVisualizer(root, available_algorithms)
    root.mainloop()

if __name__ == "__main__":
    main()
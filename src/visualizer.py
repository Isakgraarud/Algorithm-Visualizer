import math
import tkinter as tk
import random
from src import constants as c


class SortingVisualizer:
    def __init__(self, screen, algorithms):
        self.screen = screen
        self.screen.title(c.WINDOW_TITLE)
        self.data = []
        self.is_sorting = False

        self.algorithms = algorithms
        self.selected_algo_name = tk.StringVar(value=list(algorithms.keys())[0])

        self._setup_ui()
        self.generate_data()

    def _setup_ui(self):
        self.canvas = tk.Canvas(self.screen, width=c.SCREEN_WIDTH, height=c.SCREEN_HEIGHT, bg=c.BG_COLOR)
        self.canvas.pack(pady=10)

        ctrl_frame = tk.Frame(self.screen)
        ctrl_frame.pack(fill=tk.X, padx=20, pady=5)

        tk.Label(ctrl_frame, text="Algorithm:").pack(side=tk.LEFT)
        algo_menu = tk.OptionMenu(ctrl_frame, self.selected_algo_name, *self.algorithms.keys())
        algo_menu.pack(side=tk.LEFT, padx=10)

        self.shuffle_btn = tk.Button(ctrl_frame, text="Shuffle", command=self.generate_data)
        self.shuffle_btn.pack(side=tk.LEFT, padx=5)

        self.sort_btn = tk.Button(ctrl_frame, text="Start Sorting", command=self.start_sort)
        self.sort_btn.pack(side=tk.LEFT, padx=5)

        self.reset_btn = tk.Button(ctrl_frame, text="Reset", command=self.reset_visualization)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

    def reset_visualization(self):
        self.is_sorting = False
        self.canvas.delete("all")
        self.generate_data()

    def generate_data(self):
        if self.is_sorting: return
        self.data = [random.randint(c.MIN_VAL, c.MAX_VAL) for _ in range(c.NR_OF_ELEMENTS)]
        self.draw_data([c.BAR_DEFAULT_COLOR for _ in range(len(self.data))])

    def draw_data(self, color_list):
        self.canvas.delete("all")
        bar_width = c.SCREEN_WIDTH / c.NR_OF_ELEMENTS
        for i, val in enumerate(self.data):
            x0, y0 = i * bar_width, c.SCREEN_HEIGHT - val
            x1, y1 = (i + 1) * bar_width, c.SCREEN_HEIGHT
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_list[i], outline=c.BAR_OUTLINE_COLOR)
        self.screen.update()

    def animate_sort(self, generator):
        if not self.is_sorting:
            return
        try:
            data_state, highlights = next(generator)
            colors = [c.BAR_DEFAULT_COLOR] * len(self.data)
            for idx in highlights:
                if 0 <= idx < len(colors):
                    colors[idx] = c.BAR_ACTIVE_COLOR
            self.draw_data(colors)
            delay = max(0, int(c.DELAY_CONST / math.log2(len(self.data) + 1)))
            self.screen.after(delay, lambda: self.animate_sort(generator))
        except StopIteration:
            self.draw_data([c.BAR_SORTED_COLOR for _ in range(len(self.data))])
            self.is_sorting = False

    def start_sort(self):
        if self.is_sorting: return
        self.is_sorting = True
        algo_class = self.algorithms[self.selected_algo_name.get()]
        self.animate_sort(algo_class.run(self.data))
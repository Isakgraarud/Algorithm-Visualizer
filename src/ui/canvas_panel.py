import tkinter as tk
from src import constants as c


class CanvasPanel(tk.Frame):
    def __init__(self, parent, width: int, height: int, **kwargs):
        super().__init__(parent, bg=c.PANEL_BG, **kwargs)
        self._width = width
        self._height = height
        self._last_args = None
        self._canvas = tk.Canvas(self, width=width, height=height,
                                  bg=c.BG_COLOR, highlightthickness=0)
        self._canvas.pack(fill=tk.BOTH, expand=True)
        self._canvas.bind("<Configure>", self._on_resize)

    def _on_resize(self, event):
        self._width = event.width
        self._height = event.height
        if self._last_args is not None:
            self.draw(*self._last_args)

    def draw(self, data: list, color_map: dict, sorted_set: set = None):
        self._last_args = (data, color_map, sorted_set)
        self._canvas.delete("all")
        n = len(data)
        if n == 0:
            return
        bar_w = self._width / n
        scale = self._height / c.MAX_VAL
        ss = sorted_set or set()
        for i, val in enumerate(data):
            x0 = i * bar_w
            x1 = (i + 1) * bar_w
            y0 = self._height - int(val * scale)
            y1 = self._height
            role = c.ROLE_SORTED if i in ss else color_map.get(i, c.ROLE_DEFAULT)
            color = c.ROLE_COLORS.get(role, c.BAR_DEFAULT_COLOR)
            self._canvas.create_rectangle(x0, y0, x1, y1,
                                           fill=color, outline=c.BAR_OUTLINE_COLOR)

    def draw_all_sorted(self, data: list):
        self.draw(data, {}, set(range(len(data))))

    def draw_default(self, data: list):
        self.draw(data, {})

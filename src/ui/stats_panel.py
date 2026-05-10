import time
import tkinter as tk
from src import constants as c


class StatsPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        bg = kwargs.pop("bg", c.PANEL_BG)
        fg = kwargs.pop("fg", c.PANEL_FG)
        super().__init__(parent, bg=bg, **kwargs)
        self._fg = fg
        self._bg = bg
        self._start_time: float | None = None
        self._timer_id = None
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self, text="Statistics", bg=self._bg, fg=self._fg,
                 font=c.MONO_FONT_BOLD).pack(anchor="w")
        self._cmp_var  = tk.StringVar(value="Comparisons:  0")
        self._swap_var = tk.StringVar(value="Swaps:        0")
        self._time_var = tk.StringVar(value="Time:         0.000 s")
        for var in (self._cmp_var, self._swap_var, self._time_var):
            tk.Label(self, textvariable=var, bg=self._bg, fg=self._fg,
                     font=c.MONO_FONT).pack(anchor="w")

    def update(self, comparisons: int, swaps: int):
        self._cmp_var.set(f"Comparisons:  {comparisons:,}")
        self._swap_var.set(f"Swaps:        {swaps:,}")

    def start_timer(self):
        self.stop_timer()
        self._start_time = time.perf_counter()
        self._tick()

    def stop_timer(self):
        if self._timer_id is not None:
            self.after_cancel(self._timer_id)
            self._timer_id = None

    def _tick(self):
        if self._start_time is not None:
            elapsed = time.perf_counter() - self._start_time
            self._time_var.set(f"Time:         {elapsed:.3f} s")
            self._timer_id = self.after(50, self._tick)

    def reset(self):
        self.stop_timer()
        self._start_time = None
        self._cmp_var.set("Comparisons:  0")
        self._swap_var.set("Swaps:        0")
        self._time_var.set("Time:         0.000 s")

import tkinter as tk
from src import constants as c

# Fallback if an algorithm doesn't define COMPLEXITY
_UNKNOWN = {"best": "—", "average": "—", "worst": "—", "space": "—"}


class ComplexityPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        bg = kwargs.pop("bg", c.PANEL_BG)
        fg = kwargs.pop("fg", c.PANEL_FG)
        super().__init__(parent, bg=bg, **kwargs)
        self._bg = bg
        self._fg = fg
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self, text="Complexity", bg=self._bg, fg=self._fg,
                 font=c.MONO_FONT_BOLD).pack(anchor="w")
        self._name_var  = tk.StringVar(value="")
        self._best_var  = tk.StringVar(value="Best:    —")
        self._avg_var   = tk.StringVar(value="Average: —")
        self._worst_var = tk.StringVar(value="Worst:   —")
        self._space_var = tk.StringVar(value="Space:   —")
        tk.Label(self, textvariable=self._name_var,
                 bg=self._bg, fg=c.BAR_DEFAULT_COLOR, font=c.MONO_FONT_BOLD).pack(anchor="w")
        for var, color in (
            (self._best_var,  c.BAR_SORTED_COLOR),
            (self._avg_var,   c.BAR_PIVOT_COLOR),
            (self._worst_var, c.BAR_ACTIVE_COLOR),
            (self._space_var, c.BAR_MIN_COLOR),
        ):
            tk.Label(self, textvariable=var, bg=self._bg, fg=color,
                     font=c.MONO_FONT).pack(anchor="w")

    def update(self, algo_name: str, complexity: dict | None):
        d = complexity or _UNKNOWN
        self._name_var.set(algo_name)
        self._best_var.set(f"Best:    {d.get('best',  '—')}")
        self._avg_var.set( f"Average: {d.get('average','—')}")
        self._worst_var.set(f"Worst:   {d.get('worst', '—')}")
        self._space_var.set(f"Space:   {d.get('space', '—')}")

import tkinter as tk
from src import constants as c


class VariablesPanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        bg = kwargs.pop("bg", c.PANEL_BG)
        fg = kwargs.pop("fg", c.PANEL_FG)
        super().__init__(parent, bg=bg, **kwargs)
        self._bg = bg
        self._fg = fg
        self._labels: dict[str, tuple[tk.StringVar, tk.Label]] = {}
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self, text="Variables", bg=self._bg, fg=self._fg,
                 font=c.MONO_FONT_BOLD).pack(anchor="w")
        self._body = tk.Frame(self, bg=self._bg)
        self._body.pack(fill=tk.BOTH, anchor="w")

    def update(self, variables: dict):
        current = set(variables.keys())
        existing = set(self._labels.keys())

        for name in existing - current:
            self._labels[name][1].destroy()
            del self._labels[name]

        for name, value in variables.items():
            formatted = f"{name} = {value}"
            if name in self._labels:
                self._labels[name][0].set(formatted)
            else:
                var = tk.StringVar(value=formatted)
                lbl = tk.Label(self._body, textvariable=var,
                                bg=self._bg, fg="#f39c12", font=c.MONO_FONT)
                lbl.pack(anchor="w")
                self._labels[name] = (var, lbl)

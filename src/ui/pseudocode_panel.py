import tkinter as tk
from src import constants as c


class PseudocodePanel(tk.Frame):
    def __init__(self, parent, **kwargs):
        bg = kwargs.pop("bg", c.PANEL_BG)
        fg = kwargs.pop("fg", c.PANEL_FG)
        super().__init__(parent, bg=bg, **kwargs)
        self._bg = bg
        self._fg = fg
        self._lines: list[str] = []
        self._current_line = -1
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self, text="Pseudocode", bg=self._bg, fg=self._fg,
                 font=c.MONO_FONT_BOLD).pack(anchor="w")
        self._text = tk.Text(
            self, font=c.MONO_FONT, state="disabled", width=38, height=14,
            wrap="none", bg=c.BG_COLOR, fg=self._fg, relief=tk.FLAT,
            insertbackground=self._fg,
        )
        self._text.pack(fill=tk.BOTH, expand=True)
        self._text.tag_configure("highlight", background=c.BAR_PIVOT_COLOR, foreground="#0d1117")
        self._text.tag_configure("normal", background=c.BG_COLOR, foreground=self._fg)

    def set_pseudocode(self, lines: list[str]):
        self._lines = lines
        self._current_line = -1
        self._text.configure(state="normal")
        self._text.delete("1.0", tk.END)
        for i, line in enumerate(lines):
            self._text.insert(tk.END, f"{i+1:2d}  {line}\n")
        self._text.configure(state="disabled")

    def highlight_line(self, line_index: int):
        if line_index == self._current_line:
            return
        self._current_line = line_index
        self._text.configure(state="normal")
        self._text.tag_remove("highlight", "1.0", tk.END)
        if 0 <= line_index < len(self._lines):
            start = f"{line_index + 1}.0"
            end   = f"{line_index + 1}.end"
            self._text.tag_add("highlight", start, end)
        self._text.configure(state="disabled")

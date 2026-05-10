import tkinter as tk
from src import constants as c


class LogPanel(tk.Frame):
    MAX_LINES = 300

    def __init__(self, parent, **kwargs):
        bg = kwargs.pop("bg", c.PANEL_BG)
        fg = kwargs.pop("fg", c.PANEL_FG)
        super().__init__(parent, bg=bg, **kwargs)
        self._bg = bg
        self._fg = fg
        self._line_count = 0
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self, text="Log", bg=self._bg, fg=self._fg,
                 font=c.MONO_FONT_BOLD).pack(anchor="w")
        frame = tk.Frame(self, bg=self._bg)
        frame.pack(fill=tk.BOTH, expand=True)
        sb = tk.Scrollbar(frame, bg=self._bg)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self._text = tk.Text(
            frame, font=c.MONO_FONT, height=5, wrap="word",
            state="disabled", bg=c.BG_COLOR, fg=self._fg,
            insertbackground=self._fg, relief=tk.FLAT,
            yscrollcommand=sb.set,
        )
        self._text.pack(fill=tk.BOTH, expand=True)
        sb.config(command=self._text.yview)

    def append(self, message: str):
        if not message:
            return
        self._text.configure(state="normal")
        self._text.insert(tk.END, f"› {message}\n")
        self._line_count += 1
        if self._line_count > self.MAX_LINES:
            self._text.delete("1.0", "2.0")
            self._line_count -= 1
        self._text.see(tk.END)
        self._text.configure(state="disabled")

    def clear(self):
        self._text.configure(state="normal")
        self._text.delete("1.0", tk.END)
        self._text.configure(state="disabled")
        self._line_count = 0

import random
import tkinter as tk
from dataclasses import dataclass, field

from src import constants as c
from src.sort_step import SortStep
from src.sounds import SoundPlayer
from src.ui.canvas_panel import CanvasPanel
from src.ui.log_panel import LogPanel
from src.ui.stats_panel import StatsPanel
from src.ui.pseudocode_panel import PseudocodePanel
from src.ui.variables_panel import VariablesPanel
from src.ui.complexity_panel import ComplexityPanel

PRESETS = ["Random", "Sorted", "Reversed", "Nearly Sorted", "Few Unique"]


@dataclass
class _HistoryState:
    data: list
    color_map: dict
    sorted_set: set
    variables: dict
    pseudocode_line: int
    log: str
    comparisons: int
    swaps: int


def _coerce(step, data) -> SortStep:
    """Accept legacy (data, highlights) tuples as well as SortStep objects."""
    if isinstance(step, SortStep):
        return step
    if isinstance(step, tuple):
        d, highlights = step
        return SortStep(data=d, color_map={i: c.ROLE_COMPARING for i in highlights})
    return SortStep(data=data)


class SortingVisualizer:
    def __init__(self, screen, algorithms):
        self.screen = screen
        self.screen.title(c.WINDOW_TITLE)
        self.algorithms = algorithms

        self.data: list  = []
        self.data2: list = []

        self.is_sorting  = False
        self._generator  = None
        self._generator2 = None
        self._after_id   = None

        self.comparisons  = 0
        self.swaps        = 0
        self.comparisons2 = 0
        self.swaps2       = 0

        self._history: list[_HistoryState] = []
        self._history_pos = -1

        self.sound_player = SoundPlayer()

        algo_names = list(algorithms.keys())
        self.selected_algo  = tk.StringVar(value=algo_names[0])
        self.selected_algo2 = tk.StringVar(value=algo_names[min(1, len(algo_names) - 1)])
        self.speed_var   = tk.IntVar(value=c.DEFAULT_SPEED_MS)
        self.size_var    = tk.IntVar(value=c.NR_OF_ELEMENTS)
        self.preset_var  = tk.StringVar(value="Random")
        self.sound_var   = tk.BooleanVar(value=False)
        self.step_var    = tk.BooleanVar(value=False)
        self.compare_var = tk.BooleanVar(value=False)

        # Widget refs populated during _build_*
        self._content_frame    = None
        self._canvas1          = None
        self._canvas2          = None
        self._stats1           = None
        self._stats2           = None
        self._pseudo_panel     = None
        self._vars_panel       = None
        self._complexity_panel = None
        self._log_panel        = None
        self._start_btn        = None
        self._stop_btn         = None
        self._step_back_btn    = None
        self._step_fwd_btn     = None
        self._algo2_frame      = None

        self._setup_ui()
        self.generate_data()

    # ------------------------------------------------------------------ UI setup

    def _setup_ui(self):
        self.screen.configure(bg=c.PANEL_BG)
        self._build_toolbar()
        self._build_layout()

    def _build_toolbar(self):
        tb = tk.Frame(self.screen, bg=c.TOOLBAR_BG, pady=5)
        tb.pack(fill=tk.X, side=tk.TOP)

        # ---- row 1: selectors & sliders ----
        row1 = tk.Frame(tb, bg=c.TOOLBAR_BG)
        row1.pack(fill=tk.X, padx=8)
        row1.columnconfigure(20, weight=1)

        def lbl(parent, text):
            return tk.Label(parent, text=text, bg=c.TOOLBAR_BG, fg=c.PANEL_FG,
                            font=c.UI_FONT)

        def omenu(parent, var, values, cmd=None, width=14, color=c.BUTTON_BG):
            m = tk.OptionMenu(parent, var, *values, command=cmd)
            m.config(font=c.UI_FONT, bg=color, fg=c.BUTTON_FG,
                     activebackground=c.BUTTON_HOVER,
                     highlightthickness=0, relief=tk.FLAT, width=width)
            m["menu"].config(font=c.UI_FONT, bg=c.PANEL_BG, fg=c.PANEL_FG)
            return m

        col = 0
        lbl(row1, "Algorithm 1:").grid(row=0, column=col, sticky="w"); col += 1
        omenu(row1, self.selected_algo, self.algorithms.keys(),
              cmd=self._on_algo_change).grid(row=0, column=col, padx=(2, 10)); col += 1

        # algo2 — hidden until compare mode on
        self._algo2_frame = tk.Frame(row1, bg=c.TOOLBAR_BG)
        self._algo2_frame.grid(row=0, column=col, padx=(0, 10)); col += 1
        lbl(self._algo2_frame, "vs.").pack(side=tk.LEFT, padx=(0, 4))
        omenu(self._algo2_frame, self.selected_algo2, self.algorithms.keys(),
              color=c.BUTTON_BG).pack(side=tk.LEFT)
        self._algo2_frame.grid_remove()

        lbl(row1, "Preset:").grid(row=0, column=col, sticky="w"); col += 1
        omenu(row1, self.preset_var, PRESETS,
              cmd=lambda _: self.generate_data(), width=12).grid(
            row=0, column=col, padx=(2, 10)); col += 1

        lbl(row1, "Speed:").grid(row=0, column=col, sticky="w"); col += 1
        tk.Scale(row1, from_=0, to=500, orient=tk.HORIZONTAL,
                 variable=self.speed_var, length=110,
                 bg=c.TOOLBAR_BG, fg=c.PANEL_FG, troughcolor=c.SLIDER_TROUGH,
                 highlightthickness=0, showvalue=False).grid(
            row=0, column=col, padx=(2, 2)); col += 1
        lbl(row1, "Slow").grid(row=0, column=col, padx=(0, 12)); col += 1

        lbl(row1, "Size:").grid(row=0, column=col, sticky="w"); col += 1
        tk.Scale(row1, from_=10, to=300, orient=tk.HORIZONTAL,
                 variable=self.size_var, length=110,
                 bg=c.TOOLBAR_BG, fg=c.PANEL_FG, troughcolor=c.SLIDER_TROUGH,
                 highlightthickness=0, showvalue=True).grid(
            row=0, column=col, padx=(2, 12)); col += 1

        # ---- row 2: action buttons ----
        row2 = tk.Frame(tb, bg=c.TOOLBAR_BG)
        row2.pack(fill=tk.X, padx=8, pady=(4, 0))

        def btn(text, cmd, color=None, state=tk.NORMAL):
            b = tk.Button(row2, text=text, command=cmd, font=c.UI_FONT,
                          bg=color or c.BUTTON_BG, fg=c.BUTTON_FG,
                          activebackground=c.BUTTON_HOVER,
                          relief=tk.FLAT, padx=10, pady=3, state=state)
            b.pack(side=tk.LEFT, padx=3)
            return b

        def sep():
            tk.Frame(row2, width=1, bg=c.SEPARATOR_COLOR).pack(
                side=tk.LEFT, fill=tk.Y, padx=6, pady=3)

        btn("Shuffle", self.generate_data, color=c.BUTTON_BG)
        self._start_btn     = btn("▶  Start", self.start_sort,     color=c.ACTION_BG)
        self._stop_btn      = btn("■  Stop",  self.stop_sort,      color=c.BUTTON_BG, state=tk.DISABLED)
        sep()
        self._step_back_btn = btn("◀  Back",  self.step_backward,  color=c.BUTTON_BG, state=tk.DISABLED)
        self._step_fwd_btn  = btn("▶  Step",  self.step_forward,   color=c.BUTTON_BG, state=tk.DISABLED)
        sep()
        btn("Reset", self.reset_visualization, color=c.DANGER_BG)
        sep()

        def ck(text, var, cmd=None):
            tk.Checkbutton(row2, text=text, variable=var,
                           bg=c.TOOLBAR_BG, fg=c.PANEL_FG,
                           selectcolor=c.PANEL_BG, activebackground=c.TOOLBAR_BG,
                           font=c.UI_FONT, command=cmd).pack(side=tk.LEFT, padx=4)

        ck("Sound",        self.sound_var)
        ck("Step Mode",    self.step_var,    self._on_step_mode_toggle)
        ck("Compare Mode", self.compare_var, self._on_compare_mode_toggle)

    def _build_layout(self):
        if self._content_frame:
            self._content_frame.destroy()
        if self.compare_var.get():
            self._build_comparison_layout()
        else:
            self._build_normal_layout()

    def _build_normal_layout(self):
        self._content_frame = tk.Frame(self.screen, bg=c.PANEL_BG)
        self._content_frame.pack(fill=tk.BOTH, expand=True)

        main = tk.Frame(self._content_frame, bg=c.PANEL_BG)
        main.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        # Canvas
        self._canvas1 = CanvasPanel(main, c.SCREEN_WIDTH, c.SCREEN_HEIGHT)
        self._canvas1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 6))

        # Right info panel
        right = tk.Frame(main, bg=c.PANEL_BG, width=c.RIGHT_PANEL_WIDTH)
        right.pack(side=tk.LEFT, fill=tk.BOTH)
        right.pack_propagate(False)

        self._complexity_panel = ComplexityPanel(right, bg=c.PANEL_BG, fg=c.PANEL_FG)
        self._complexity_panel.pack(fill=tk.X, pady=(0, 4))

        tk.Frame(right, height=1, bg=c.SEPARATOR_COLOR).pack(fill=tk.X, pady=3)

        self._stats1 = StatsPanel(right, bg=c.PANEL_BG, fg=c.PANEL_FG)
        self._stats1.pack(fill=tk.X, pady=(0, 4))

        tk.Frame(right, height=1, bg=c.SEPARATOR_COLOR).pack(fill=tk.X, pady=3)

        self._vars_panel = VariablesPanel(right, bg=c.PANEL_BG, fg=c.PANEL_FG)
        self._vars_panel.pack(fill=tk.X, pady=(0, 4))

        tk.Frame(right, height=1, bg=c.SEPARATOR_COLOR).pack(fill=tk.X, pady=3)

        self._pseudo_panel = PseudocodePanel(right, bg=c.PANEL_BG, fg=c.PANEL_FG)
        self._pseudo_panel.pack(fill=tk.BOTH, expand=True)

        # Log
        self._log_panel = LogPanel(self._content_frame, bg=c.PANEL_BG, fg=c.PANEL_FG)
        self._log_panel.pack(fill=tk.X, padx=6, pady=(0, 6))

        self._canvas2 = None
        self._stats2  = None
        self._on_algo_change(self.selected_algo.get())

    def _build_comparison_layout(self):
        self._content_frame = tk.Frame(self.screen, bg=c.PANEL_BG)
        self._content_frame.pack(fill=tk.BOTH, expand=True)

        area = tk.Frame(self._content_frame, bg=c.PANEL_BG)
        area.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        def col_frame(parent):
            f = tk.Frame(parent, bg=c.PANEL_BG)
            f.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=3)
            return f

        left_col  = col_frame(area)
        right_col = col_frame(area)

        tk.Label(left_col, textvariable=self.selected_algo,
                 bg=c.PANEL_BG, fg="#4a90d9", font=c.MONO_FONT_BOLD).pack()
        self._canvas1 = CanvasPanel(left_col, c.COMPARE_CANVAS_WIDTH, c.COMPARE_CANVAS_HEIGHT)
        self._canvas1.pack(fill=tk.BOTH, expand=True)
        self._stats1 = StatsPanel(left_col, bg=c.PANEL_BG, fg=c.PANEL_FG)
        self._stats1.pack(fill=tk.X)

        tk.Label(right_col, textvariable=self.selected_algo2,
                 bg=c.PANEL_BG, fg="#9b59b6", font=c.MONO_FONT_BOLD).pack()
        self._canvas2 = CanvasPanel(right_col, c.COMPARE_CANVAS_WIDTH, c.COMPARE_CANVAS_HEIGHT)
        self._canvas2.pack(fill=tk.BOTH, expand=True)
        self._stats2 = StatsPanel(right_col, bg=c.PANEL_BG, fg=c.PANEL_FG)
        self._stats2.pack(fill=tk.X)

        self._log_panel = LogPanel(self._content_frame, bg=c.PANEL_BG, fg=c.PANEL_FG)
        self._log_panel.pack(fill=tk.X, padx=6, pady=(0, 6))

        self._pseudo_panel     = None
        self._vars_panel       = None
        self._complexity_panel = None

    # ---------------------------------------------------------------- toolbar callbacks

    def _on_algo_change(self, algo_name: str):
        algo_class = self.algorithms.get(algo_name)
        if self._complexity_panel:
            self._complexity_panel.update(algo_name, getattr(algo_class, "COMPLEXITY", None))
        if self._pseudo_panel:
            self._pseudo_panel.set_pseudocode(getattr(algo_class, "PSEUDOCODE", []))

    def _on_step_mode_toggle(self):
        step = self.step_var.get()
        if step:
            self._step_back_btn.config(state=tk.NORMAL)
            self._step_fwd_btn.config(state=tk.NORMAL)
            self._start_btn.config(state=tk.DISABLED)
        else:
            self._step_back_btn.config(state=tk.DISABLED)
            self._step_fwd_btn.config(state=tk.DISABLED)
            self._start_btn.config(state=tk.NORMAL)

    def _on_compare_mode_toggle(self):
        if self.is_sorting:
            self.stop_sort()
        if self.compare_var.get():
            self._algo2_frame.grid()
            self.step_var.set(False)
            self._on_step_mode_toggle()
        else:
            self._algo2_frame.grid_remove()
        self._build_layout()
        self.generate_data()

    # ---------------------------------------------------------------- data generation

    def generate_data(self):
        if self.is_sorting:
            return
        n = self.size_var.get()
        preset = self.preset_var.get()

        if preset == "Sorted":
            step = max(1, (c.MAX_VAL - c.MIN_VAL) // n)
            data = [min(c.MAX_VAL, c.MIN_VAL + i * step) for i in range(n)]
        elif preset == "Reversed":
            step = max(1, (c.MAX_VAL - c.MIN_VAL) // n)
            data = [max(c.MIN_VAL, c.MAX_VAL - i * step) for i in range(n)]
        elif preset == "Nearly Sorted":
            step = max(1, (c.MAX_VAL - c.MIN_VAL) // n)
            data = [min(c.MAX_VAL, c.MIN_VAL + i * step) for i in range(n)]
            for _ in range(max(1, n // 10)):
                i, j = random.randint(0, n - 1), random.randint(0, n - 1)
                data[i], data[j] = data[j], data[i]
        elif preset == "Few Unique":
            anchors = [random.randint(c.MIN_VAL, c.MAX_VAL) for _ in range(5)]
            data = [random.choice(anchors) for _ in range(n)]
        else:
            data = [random.randint(c.MIN_VAL, c.MAX_VAL) for _ in range(n)]

        self.data = data
        if self.compare_var.get():
            self.data2 = list(data)

        self._refresh_display()

    def _refresh_display(self):
        if self._canvas1:
            self._canvas1.draw_default(self.data)
        if self._canvas2 and self.data2:
            self._canvas2.draw_default(self.data2)
        self.screen.update_idletasks()

    # ---------------------------------------------------------------- sort control

    def start_sort(self):
        if self.is_sorting:
            return
        if self.step_var.get():
            self._init_step_mode()
            return

        self._reset_stats()
        self.is_sorting = True
        if self._log_panel:
            self._log_panel.clear()

        algo_class = self.algorithms[self.selected_algo.get()]
        self._generator = algo_class.run(self.data)

        if self.compare_var.get():
            algo2 = self.algorithms[self.selected_algo2.get()]
            self._generator2 = algo2.run(self.data2)

        self._start_btn.config(state=tk.DISABLED)
        self._stop_btn.config(state=tk.NORMAL)

        if self._stats1:
            self._stats1.start_timer()
        if self._stats2:
            self._stats2.start_timer()

        self._animate()

    def _animate(self):
        if not self.is_sorting:
            return

        done1 = self._tick_generator(self._generator, self._canvas1, self._stats1,
                                      self.data, primary=True)
        done2 = True
        if self._generator2 and self._canvas2:
            done2 = self._tick_generator(self._generator2, self._canvas2, self._stats2,
                                          self.data2, primary=False)

        if done1:
            self._canvas1.draw_all_sorted(self.data)
        if self._canvas2 and done2:
            self._canvas2.draw_all_sorted(self.data2)

        both_done = done1 and (done2 or not self.compare_var.get())
        if both_done:
            self._finish_sort()
            return

        self._after_id = self.screen.after(self.speed_var.get(), self._animate)

    def _tick_generator(self, gen, canvas, stats, data, *, primary) -> bool:
        """Advance generator one step. Returns True when exhausted."""
        try:
            raw = next(gen)
        except StopIteration:
            return True

        step = _coerce(raw, data)

        if primary:
            self.comparisons += step.comparisons_delta
            self.swaps       += step.swaps_delta
            if stats:
                stats.update(self.comparisons, self.swaps)
            if self._vars_panel and step.variables:
                self._vars_panel.update(step.variables)
            if self._pseudo_panel and step.pseudocode_line >= 0:
                self._pseudo_panel.highlight_line(step.pseudocode_line)
            if self._log_panel and step.log:
                self._log_panel.append(step.log)
        else:
            self.comparisons2 += step.comparisons_delta
            self.swaps2       += step.swaps_delta
            if stats:
                stats.update(self.comparisons2, self.swaps2)
            if self._log_panel and step.log:
                self._log_panel.append(f"[Algo 2] {step.log}")

        if canvas:
            canvas.draw(step.data, step.color_map, step.sorted_set)

        if self.sound_var.get() and (step.comparisons_delta or step.swaps_delta) and step.color_map:
            idx = next(iter(step.color_map))
            if idx < len(step.data):
                freq = self.sound_player.value_to_freq(step.data[idx])
                self.sound_player.play(freq)

        return False

    def stop_sort(self):
        if self._after_id:
            self.screen.after_cancel(self._after_id)
            self._after_id = None
        self.is_sorting  = False
        self._generator  = None
        self._generator2 = None
        if self._stats1:
            self._stats1.stop_timer()
        if self._stats2:
            self._stats2.stop_timer()
        self._start_btn.config(state=tk.NORMAL)
        self._stop_btn.config(state=tk.DISABLED)

    def _finish_sort(self):
        self.is_sorting = False
        if self._stats1:
            self._stats1.stop_timer()
        if self._stats2:
            self._stats2.stop_timer()
        self._start_btn.config(state=tk.NORMAL)
        self._stop_btn.config(state=tk.DISABLED)
        if self._log_panel:
            self._log_panel.append("Sort complete!")

    def reset_visualization(self):
        self.stop_sort()
        self._history.clear()
        self._history_pos = -1
        self._reset_stats()
        if self._log_panel:
            self._log_panel.clear()
        if self._vars_panel:
            self._vars_panel.update({})
        if self._pseudo_panel:
            self._pseudo_panel.highlight_line(-1)
        self.generate_data()

    def _reset_stats(self):
        self.comparisons  = 0
        self.swaps        = 0
        self.comparisons2 = 0
        self.swaps2       = 0
        if self._stats1:
            self._stats1.reset()
        if self._stats2:
            self._stats2.reset()

    # ---------------------------------------------------------------- step mode

    def _init_step_mode(self):
        self._reset_stats()
        self._history.clear()
        self._history_pos = -1
        self.is_sorting = True
        if self._log_panel:
            self._log_panel.clear()
        algo_class = self.algorithms[self.selected_algo.get()]
        self._generator = algo_class.run(self.data)
        self.step_forward()

    def step_forward(self):
        if not self.is_sorting and not self._generator:
            self._init_step_mode()
            return

        if self._history_pos < len(self._history) - 1:
            self._history_pos += 1
            self._show_history(self._history[self._history_pos])
            return

        if self._generator is None:
            return
        try:
            raw = next(self._generator)
        except StopIteration:
            if self._canvas1:
                self._canvas1.draw_all_sorted(self.data)
            self._finish_sort()
            return

        step = _coerce(raw, self.data)
        self.comparisons += step.comparisons_delta
        self.swaps       += step.swaps_delta

        state = _HistoryState(
            data=list(step.data),
            color_map=dict(step.color_map),
            sorted_set=set(step.sorted_set),
            variables=dict(step.variables),
            pseudocode_line=step.pseudocode_line,
            log=step.log,
            comparisons=self.comparisons,
            swaps=self.swaps,
        )
        if len(self._history) < c.HISTORY_MAX:
            self._history.append(state)
        self._history_pos = len(self._history) - 1

        self._show_history(state)

        if self.sound_var.get() and (step.comparisons_delta or step.swaps_delta) and step.color_map:
            idx = next(iter(step.color_map))
            if idx < len(step.data):
                freq = self.sound_player.value_to_freq(step.data[idx])
                self.sound_player.play(freq)

    def step_backward(self):
        if self._history_pos > 0:
            self._history_pos -= 1
            self._show_history(self._history[self._history_pos])

    def _show_history(self, state: _HistoryState):
        if self._canvas1:
            self._canvas1.draw(state.data, state.color_map, state.sorted_set)
        if self._stats1:
            self._stats1.update(state.comparisons, state.swaps)
        if self._vars_panel:
            self._vars_panel.update(state.variables)
        if self._pseudo_panel:
            self._pseudo_panel.highlight_line(state.pseudocode_line)
        if self._log_panel and state.log:
            self._log_panel.append(state.log)
        self.screen.update_idletasks()

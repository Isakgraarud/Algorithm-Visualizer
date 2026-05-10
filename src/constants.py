# --- Window ---
WINDOW_TITLE = "Algorithm Visualizer"
WINDOW_WIDTH = 1160
WINDOW_HEIGHT = 660

# --- Canvas ---
SCREEN_WIDTH = 790
SCREEN_HEIGHT = 380
COMPARE_CANVAS_WIDTH = 555
COMPARE_CANVAS_HEIGHT = 345
RIGHT_PANEL_WIDTH = 330

# --- Data ---
NR_OF_ELEMENTS = 80
MIN_VAL = 20
MAX_VAL = 340

# --- Animation ---
DEFAULT_SPEED_MS = 30
HISTORY_MAX = 10000

# --- Canvas background ---
BG_COLOR = "#0d1117"

# --- Bar colors (by semantic role) ---
BAR_DEFAULT_COLOR = "#4493f8"   # blue
BAR_ACTIVE_COLOR  = "#f47067"   # coral-red  — comparing
BAR_SORTED_COLOR  = "#3fb950"   # green      — fully sorted
BAR_PIVOT_COLOR   = "#e3b341"   # amber/gold — pivot
BAR_SWAP_COLOR    = "#fb8f44"   # orange     — swapping
BAR_MIN_COLOR     = "#bc8cff"   # violet     — minimum / special marker
BAR_OUTLINE_COLOR = "#0d1117"   # same as bg → no visible outline

# --- UI chrome ---
PANEL_BG      = "#161b22"   # right-side panels
TOOLBAR_BG    = "#21262d"   # top toolbar
PANEL_FG      = "#c9d1d9"   # primary text
BUTTON_BG     = "#2d333b"   # dropdowns & default buttons
BUTTON_FG     = "#000000"   # button / dropdown text
BUTTON_HOVER  = "#444c56"   # hover state
ACTION_BG     = "#1f6feb"   # Start / primary action buttons (blue)
ACTION_HOVER  = "#388bfd"
DANGER_BG     = "#b62324"   # Reset / destructive buttons
SLIDER_TROUGH = "#2d333b"
SEPARATOR_COLOR = "#30363d"

# --- Fonts ---
UI_FONT        = ("Segoe UI", 9)
UI_FONT_SMALL  = ("Segoe UI", 8)
MONO_FONT      = ("Consolas", 9)
MONO_FONT_BOLD = ("Consolas", 10, "bold")

# --- Color role mapping ---
ROLE_DEFAULT   = "default"
ROLE_COMPARING = "comparing"
ROLE_PIVOT     = "pivot"
ROLE_SWAP      = "swap"
ROLE_SORTED    = "sorted"
ROLE_MIN       = "min"

ROLE_COLORS = {
    ROLE_DEFAULT:   BAR_DEFAULT_COLOR,
    ROLE_COMPARING: BAR_ACTIVE_COLOR,
    ROLE_PIVOT:     BAR_PIVOT_COLOR,
    ROLE_SWAP:      BAR_SWAP_COLOR,
    ROLE_SORTED:    BAR_SORTED_COLOR,
    ROLE_MIN:       BAR_MIN_COLOR,
}

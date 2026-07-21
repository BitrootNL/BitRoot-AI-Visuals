import os
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

# Where to store the plots
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "plots") + os.sep
os.makedirs(OUTPUT_PATH, exist_ok=True)


def output_path(filename: str) -> str:
    """Return a writable output path and create any required parent directories."""
    full_path = os.path.join(OUTPUT_PATH, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path

# Bitroot colour reference palette
BITROOT_PALETTE = {
    "primary": "#269FBA",
    "secondary": "#5C78D9",
    "tertiary": "#A3D979",
    "highlight": "#B1325D",
    "success": "#3DB873",
    "warning": "#D4A843",
    "error": "#C94A3E",
    "info": "#4D8FC9",
    "text": "#2D3333",
    "secondary_text": "#4D5C5C",
    "background": "#F8FAFA",
    "card_background": "#FFFFFF",
    "grid": "#D8E0E0",
}


def _tint_color(color: str, amount: float) -> str:
    """Return a lighter tint of a color based on the Bitroot palette."""
    r, g, b = mcolors.to_rgb(color)
    return mcolors.to_hex((1 - (1 - r) * (1 - amount), 1 - (1 - g) * (1 - amount), 1 - (1 - b) * (1 - amount)))


BITROOT_PALETTE.update({
    "primary_light": _tint_color(BITROOT_PALETTE["primary"], 0.35),
    "primary_soft": _tint_color(BITROOT_PALETTE["primary"], 0.18),
    "secondary_light": _tint_color(BITROOT_PALETTE["secondary"], 0.25),
    "secondary_soft": _tint_color(BITROOT_PALETTE["secondary"], 0.12),
    "tertiary_light": _tint_color(BITROOT_PALETTE["tertiary"], 0.25),
    "tertiary_soft": _tint_color(BITROOT_PALETTE["tertiary"], 0.12),
})

# Backward-compatible palette aliases used by the existing examples
COLOR_PALETTE = {
    "base_colors": {
        "dark_green": BITROOT_PALETTE["primary"],
        "medium_green": BITROOT_PALETTE["tertiary"],
        "bright_teal": BITROOT_PALETTE["primary"],
        "bright_yellow": BITROOT_PALETTE["warning"],
    },
    "complementary_colors": {
        "deep_burgundy": BITROOT_PALETTE["highlight"],
        "warm_brown": "#8A5722",
        "rusty_red": "#7A2D2A",
        "soft_coral": "#D9746E",
    },
    "analogous_colors": {
        "deep_teal": BITROOT_PALETTE["primary"],
        "soft_green": BITROOT_PALETTE["tertiary"],
        "light_yellow": BITROOT_PALETTE["warning"],
        "golden_yellow": "#D9B23F",
    },
    "neutral_colors": {
        "white": "#FFFFFF",
        "light_gray": "#F3F7F7",
        "medium_gray": "#8A9393",
        "dark_gray": BITROOT_PALETTE["secondary_text"],
        "charcoal": BITROOT_PALETTE["text"],
    },
    "accent_colors": {
        "coral_pink": BITROOT_PALETTE["error"],
        "periwinkle_blue": BITROOT_PALETTE["secondary"],
        "mint_green": BITROOT_PALETTE["tertiary"],
        "light_beige": BITROOT_PALETTE["background"],
    },
}


def get_series_colors(count: int, start_index: int = 0):
    """Return a list of colors following the Bitroot recommended series order."""
    series = [
        BITROOT_PALETTE["primary"],
        BITROOT_PALETTE["secondary"],
        BITROOT_PALETTE["tertiary"],
        BITROOT_PALETTE["highlight"],
    ]
    return [series[(index + start_index) % len(series)] for index in range(count)]


def apply_bitroot_style(ax=None, *, background=None, text=None, grid=None, title_size=16, label_size=14):
    """Apply the Bitroot visual defaults to a Matplotlib axis."""
    if ax is None:
        ax = plt.gca()

    background = background or BITROOT_PALETTE["background"]
    text = text or BITROOT_PALETTE["text"]
    grid = grid or BITROOT_PALETTE["grid"]

    ax.set_facecolor(background)
    figure = ax.figure
    if figure is not None:
        figure.patch.set_facecolor(background)
    ax.grid(True, color=grid, linestyle="-", linewidth=0.8, alpha=0.9)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color(grid)

    ax.tick_params(colors=text, labelsize=11)
    if ax.title:
        ax.title.set_color(text)
        ax.title.set_fontsize(title_size)
    if ax.xaxis.label:
        ax.xaxis.label.set_color(text)
        ax.xaxis.label.set_fontsize(label_size)
    if ax.yaxis.label:
        ax.yaxis.label.set_color(text)
        ax.yaxis.label.set_fontsize(label_size)

    return ax


# Define a list of colors for a colour map (white to green)
CMAP_WHITE = mcolors.LinearSegmentedColormap.from_list(
    name="white_cmap",
    colors=[COLOR_PALETTE["neutral_colors"]["white"], COLOR_PALETTE["base_colors"]["medium_green"]],
    N=256,
)
CMAP_CONTRAST = mcolors.LinearSegmentedColormap.from_list(
    name="contrast_cmap",
    colors=[COLOR_PALETTE["base_colors"]["medium_green"], COLOR_PALETTE["complementary_colors"]["deep_burgundy"]],
    N=256,
)

# Colourful custom colour map
CMAP_BRAND = mcolors.LinearSegmentedColormap.from_list(
    name="bitroot_brand_cmap",
    colors=[BITROOT_PALETTE["warning"], BITROOT_PALETTE["tertiary"], BITROOT_PALETTE["primary"]],
    N=256,
)
CMAP_BITROOT = mcolors.LinearSegmentedColormap.from_list(
    name="bitroot_cmap",
    colors=[BITROOT_PALETTE["background"], BITROOT_PALETTE["primary"], BITROOT_PALETTE["secondary"]],
    N=256,
)
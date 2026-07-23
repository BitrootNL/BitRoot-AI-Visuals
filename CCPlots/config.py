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
    "white": "#F2F5F5",
    "grid": "#D8E0E0",
}


def darken_color(color: str, factor: float = 0.6) -> str:
    """Return a darker shade of a color."""
    r, g, b = mcolors.to_rgb(color)
    return mcolors.to_hex((r * factor, g * factor, b * factor))


def probability_color(probability: float, light_color: str = "primary_soft", dark_color: str = "primary") -> str:
    """Return a primary-based shade where higher probability is darker.

    Blends between two palette colors based on probability (0 -> light, 1 -> dark).
    """
    light = mcolors.to_rgb(BITROOT_PALETTE[light_color])
    dark = mcolors.to_rgb(BITROOT_PALETTE[dark_color])
    blended = tuple(light[i] + probability * (dark[i] - light[i]) for i in range(3))
    return mcolors.to_hex(blended)


def _tint_color(color: str, amount: float) -> str:
    """Return a lighter tint of a color based on the Bitroot palette."""
    r, g, b = mcolors.to_rgb(color)
    return mcolors.to_hex((1 - (1 - r) * (1 - amount), 1 - (1 - g) * (1 - amount), 1 - (1 - b) * (1 - amount)))


BITROOT_PALETTE.update({
    "primary_soft": _tint_color(BITROOT_PALETTE["primary"], 0.18),
    "primary_pale": _tint_color(BITROOT_PALETTE["primary"], 0.80),
    "secondary_light": _tint_color(BITROOT_PALETTE["secondary"], 0.25),
    "secondary_soft": _tint_color(BITROOT_PALETTE["secondary"], 0.12),
})


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

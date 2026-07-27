"""
``CCPlots.config.palette`` — Bitroot colour palette and visual styling tools.

**What this controls:**
- The shared colour palette (``BITROOT_PALETTE``) used by every plot.
- Colour derivation helpers (``darken_color``, ``probability_color``).
- The ``apply_bitroot_style()`` function that applies Bitroot theme defaults
  (background, grid, spine colours, tick parameters) to a matplotlib Axes.

**Scope: global.** Changes here affect every plot in the library.
Use ``CCPlots/plot_configs/*.json`` to tweak per-example settings instead.
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

BITROOT_PALETTE: dict[str, str] = {
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


def _tint_color(color: str, amount: float) -> str:
    r, g, b = mcolors.to_rgb(color)
    return mcolors.to_hex((1 - (1 - r) * (1 - amount), 1 - (1 - g) * (1 - amount), 1 - (1 - b) * (1 - amount)))


BITROOT_PALETTE.update({
    "primary_soft": _tint_color(BITROOT_PALETTE["primary"], 0.18),
    "primary_pale": _tint_color(BITROOT_PALETTE["primary"], 0.80),
    "secondary_light": _tint_color(BITROOT_PALETTE["secondary"], 0.25),
    "secondary_soft": _tint_color(BITROOT_PALETTE["secondary"], 0.12),
})


def darken_color(color: str, factor: float = 0.6) -> str:
    """Return a darker shade of a colour by multiplying each RGB channel by *factor*."""
    r, g, b = mcolors.to_rgb(color)
    return mcolors.to_hex((r * factor, g * factor, b * factor))


def probability_color(probability: float, light_color: str = "primary_soft", dark_color: str = "primary") -> str:
    """Blend between two palette colours based on a probability value.

    ``probability=0`` returns the *light_color*; ``probability=1`` returns *dark_color*.
    Used by bar charts to encode confidence / intensity as a monotonic gradient.
    """
    light = mcolors.to_rgb(BITROOT_PALETTE[light_color])
    dark = mcolors.to_rgb(BITROOT_PALETTE[dark_color])
    blended = tuple(light[i] + probability * (dark[i] - light[i]) for i in range(3))
    return mcolors.to_hex(blended)


def apply_bitroot_style(ax=None, *, background=None, text=None, grid=None, title_size=16, label_size=14):
    """Apply the Bitroot visual defaults to a matplotlib Axes.

    Parameters
    ----------
    ax : Axes or None
        Target axis. Defaults to ``plt.gca()``.
    background, text, grid : str or None
        Override the palette colours for this call. Falls back to palette values.
    title_size, label_size : int
        Font sizes for the title and axis labels.

    Returns the (possibly created) Axes.
    """
    if ax is None:
        ax = plt.gca()

    _bg = background or BITROOT_PALETTE["background"]
    _text = text or BITROOT_PALETTE["text"]
    _grid = grid or BITROOT_PALETTE["grid"]

    ax.set_facecolor(_bg)
    figure = ax.figure
    if figure is not None:
        figure.patch.set_facecolor(_bg)
    ax.grid(True, color=_grid, linestyle="-", linewidth=0.8, alpha=0.9)
    ax.set_axisbelow(True)

    for spine in ax.spines.values():
        spine.set_color(_grid)

    ax.tick_params(colors=_text, labelsize=11)
    if ax.title:
        ax.title.set_color(_text)
        ax.title.set_fontsize(title_size)
    if ax.xaxis.label:
        ax.xaxis.label.set_color(_text)
        ax.xaxis.label.set_fontsize(label_size)
    if ax.yaxis.label:
        ax.yaxis.label.set_color(_text)
        ax.yaxis.label.set_fontsize(label_size)

    return ax

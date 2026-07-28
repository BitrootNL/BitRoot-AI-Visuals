"""
``CCPlots.config.palette`` — Bitroot colour palette and visual styling tools.

**What this controls:**
- The shared colour palette (``BITROOT_PALETTE``) used by every plot.
- Colour derivation helpers (``tint_color``, ``shade_color``, ``darken_color``,
  ``probability_color``).
- The ``apply_bitroot_style()`` function that applies Bitroot theme defaults
  (background, grid, spine colours, tick parameters) to a matplotlib Axes.
- ``resolve_palette_key()`` — resolves strings like ``"primary"`` or
  ``"primary@tint(0.8)"`` to a hex string, used by the config-driven colour
  system.

Approach to colouring implemented from: https://maketintsandshades.com/about/.

**Scope: global.** Changes here affect every plot in the library.
Use ``CCPlots/plot_configs/*.json`` to tweak per-example settings instead.
"""

import re
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

_TINT_RE = re.compile(r"^(\w+)@tint\(([\d.]+)\)$")
_SHADE_RE = re.compile(r"^(\w+)@shade\(([\d.]+)\)$")


def _round_half_up(x: float) -> int:
    """Round to nearest integer; .5 always rounds up (away from zero)."""
    return int(x + 0.5)


def tint_color(color: str, amount: float) -> str:
    """Tint *color* toward white by *amount* (0 = no change, 1 = white).

    Each RGB channel moves toward 255:
        new = current + ((255 - current) × amount)
    Values are rounded to the nearest whole number (.5 rounds up).
    """
    r, g, b = mcolors.to_rgb(color)
    r_int = _round_half_up(r * 255 + (255 - r * 255) * amount)
    g_int = _round_half_up(g * 255 + (255 - g * 255) * amount)
    b_int = _round_half_up(b * 255 + (255 - b * 255) * amount)
    return f"#{r_int:02X}{g_int:02X}{b_int:02X}"


def shade_color(color: str, amount: float) -> str:
    """Shade *color* toward black by *amount* (0 = black, 1 = no change).

    Each RGB channel is scaled:
        new = current × amount
    Values are rounded to the nearest whole number (.5 rounds up).
    """
    r, g, b = mcolors.to_rgb(color)
    r_int = _round_half_up(r * 255 * amount)
    g_int = _round_half_up(g * 255 * amount)
    b_int = _round_half_up(b * 255 * amount)
    return f"#{r_int:02X}{g_int:02X}{b_int:02X}"


# Pre-compute common tints for quick access
BITROOT_PALETTE.update({
    "primary_soft": tint_color(BITROOT_PALETTE["primary"], 0.18),
    "primary_pale": tint_color(BITROOT_PALETTE["primary"], 0.80),
    "secondary_light": tint_color(BITROOT_PALETTE["secondary"], 0.25),
    "secondary_soft": tint_color(BITROOT_PALETTE["secondary"], 0.12),
})


def resolve_palette_key(key_spec: str) -> str:
    """Resolve a palette key or tint/shade expression to a hex colour.

    Supported forms:
        ``"primary"``               — direct palette lookup
        ``"primary@tint(0.8)"``      — tinted version
        ``"primary@shade(0.6)"``     — shaded version
        ``"#AABBCC"``                — passed through unchanged
    """
    if key_spec.startswith("#"):
        return key_spec

    m = _TINT_RE.match(key_spec)
    if m:
        base = BITROOT_PALETTE[m.group(1)]
        return tint_color(base, float(m.group(2)))

    m = _SHADE_RE.match(key_spec)
    if m:
        base = BITROOT_PALETTE[m.group(1)]
        return shade_color(base, float(m.group(2)))

    if key_spec in BITROOT_PALETTE:
        return BITROOT_PALETTE[key_spec]

    return key_spec


def darken_color(color: str, factor: float = 0.6) -> str:
    """Deprecated: use ``shade_color()`` instead. Same behaviour."""
    return shade_color(color, factor)


def probability_color(probability: float, light_color: str = "primary_soft", dark_color: str = "primary") -> str:
    """Blend between two palette colours based on a probability value.

    ``probability=0`` returns the *light_color*; ``probability=1`` returns *dark_color*.
    Used by bar charts to encode confidence / intensity as a monotonic gradient.
    """
    light = mcolors.to_rgb(resolve_palette_key(light_color))
    dark = mcolors.to_rgb(resolve_palette_key(dark_color))
    blended = tuple(light[i] + probability * (dark[i] - light[i]) for i in range(3))
    return f"#{_round_half_up(blended[0] * 255):02X}{_round_half_up(blended[1] * 255):02X}{_round_half_up(blended[2] * 255):02X}"


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

    _bg = resolve_palette_key(background) if background else BITROOT_PALETTE["background"]
    _text = resolve_palette_key(text) if text else BITROOT_PALETTE["text"]
    _grid = resolve_palette_key(grid) if grid else BITROOT_PALETTE["grid"]

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

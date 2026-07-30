"""
``CCPlots.config.palette`` — Bitroot colour palette and visual styling tools.

**What this controls:**
- The shared colour palette (``BITROOT_PALETTE``) used by every plot.  The
  palette is loaded from ``bitroot.json`` (the single source of truth derived
  from the Bitroot design system).
- Colour derivation helpers (``tint_color``, ``shade_color``).
- The ``apply_bitroot_style()`` function that applies Bitroot theme defaults
  (background, grid, spine colours, tick parameters) to a matplotlib Axes.
- ``resolve_palette_key()`` — resolves strings like ``"primary"`` or
  ``"primary@tint(0.8)"`` to a hex string, used by the config-driven colour
  system.

Approach to colouring implemented from: https://maketintsandshades.com/about/.

**Scope: global.** Changes here affect every plot in the library.
Use ``CCPlots/plot_configs/*.json`` to tweak per-example settings instead.

To add or update a colour, edit ``bitroot.json`` — do NOT hard-code hex values
in this module.
"""

import json
import os
import re
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

# ── Load palette from the shared JSON config ──────────────────────────────

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_CONFIG_PATH = os.path.join(_PROJECT_ROOT, "bitroot.json")

with open(_CONFIG_PATH, encoding="utf-8") as _f:
    _BITROOT_CONFIG = json.load(_f)

_COLORS: dict[str, dict[str, str]] = _BITROOT_CONFIG["colors"]

# Build the flat hex dict from the canonical DESIGN.md colour names.
BITROOT_PALETTE: dict[str, str] = {
    name: entry["hex"] for name, entry in _COLORS.items()
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


def _relative_luminance(hex_color: str) -> float:
    """WCAG 2.0 relative luminance of a hex colour (0 = black, 1 = white)."""
    r, g, b = mcolors.to_rgb(hex_color)
    def linearise(c: float) -> float:
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * linearise(r) + 0.7152 * linearise(g) + 0.0722 * linearise(b)


def _contrast_ratio(a: str, b: str) -> float:
    """WCAG contrast ratio between two hex colours (1–21)."""
    la = _relative_luminance(a)
    lb = _relative_luminance(b)
    lighter = max(la, lb)
    darker = min(la, lb)
    return (lighter + 0.05) / (darker + 0.05)


def contrasting_text_color(bg_color: str,
                           dark_text: str | None = None,
                           light_text: str | None = None,
                           *,
                           large: bool = False) -> str:
    """Return ``dark_text`` or ``light_text``, whichever offers better WCAG AA
    contrast against *bg_color*.

    Parameters
    ----------
    bg_color : str
        Background colour (hex, palette key, or tint/shade expression).
    dark_text : str or None
        Dark text colour.  Defaults to ``BITROOT_PALETTE["text"]``.
    light_text : str or None
        Light text colour.  Defaults to ``BITROOT_PALETTE["white"]``.
    large : bool
        If True, uses the 3:1 large-text threshold (WCAG AA).
        Otherwise uses the 4.5:1 normal-text threshold.
    """
    bg = resolve_palette_key(bg_color)
    dk = resolve_palette_key(dark_text) if dark_text else BITROOT_PALETTE["on-surface"]
    lt = resolve_palette_key(light_text) if light_text else BITROOT_PALETTE["white"]

    ratio_dk = _contrast_ratio(bg, dk)
    ratio_lt = _contrast_ratio(bg, lt)

    threshold = 3.0 if large else 4.5

    # If both pass, pick the one with the higher ratio.
    # If only one passes, use that one.
    dk_passes = ratio_dk >= threshold
    lt_passes = ratio_lt >= threshold

    if dk_passes and lt_passes:
        return dk if ratio_dk >= ratio_lt else lt
    if dk_passes:
        return dk
    if lt_passes:
        return lt
    # Neither passes — return whichever is closer (shouldn't happen with our palette)
    return dk if ratio_dk >= ratio_lt else lt


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

    _bg = resolve_palette_key(background) if background else BITROOT_PALETTE["surface"]
    _text = resolve_palette_key(text) if text else BITROOT_PALETTE["on-surface"]
    _grid = resolve_palette_key(grid) if grid else BITROOT_PALETTE["border"]

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

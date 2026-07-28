"""
``CCPlots.PlotExample`` — Abstract base class for all example plots.

Subclasses must define:
    - ``CONFIG_KEY`` (str) — matches the JSON filename in ``plot_configs/``
    - (locale text is loaded from the JSON config's ``text`` section)
    - ``main()`` — the plot generation entry point

The base class provides config-driven helpers for the common patterns
shared by most examples:
    - ``iter_locales()`` — yields ``(locale_code, labels, suffix)``
    - ``create_figure()`` — styled figure from the example's JSON config
    - ``apply_style()`` — Bitroot theme on one or more axes
    - ``save_figure()`` — saves and closes using the config's output pattern
    - ``resolve_color()`` — resolves a semantic colour name to hex
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import matplotlib.pyplot as plt

from CCPlots.config import (
    BITROOT_PALETTE,
    ExampleConfig,
    apply_bitroot_style,
    contrasting_text_color,
    load_example_config,
    output_path,
)
from CCPlots.config.palette import resolve_palette_key


class PlotExample(ABC):

    # --- Must be overridden by every concrete subclass ---
    CONFIG_KEY: str = ""

    def __init__(self) -> None:
        self._cfg: ExampleConfig | None = None

    # ------------------------------------------------------------------
    # Config access
    # ------------------------------------------------------------------

    @property
    def config(self) -> ExampleConfig:
        """The ``ExampleConfig`` loaded from ``plot_configs/{CONFIG_KEY}.json``."""
        cfg = getattr(self, "_cfg", None)
        if cfg is None:
            cfg = load_example_config(self.CONFIG_KEY)
            self._cfg = cfg
        return cfg

    # ------------------------------------------------------------------
    # Locale text  (from config JSON, falling back to class attr)
    # ------------------------------------------------------------------

    @property
    def locale_text(self) -> dict[str, dict[str, Any]]:
        """Locale text from the JSON config."""
        return self.config.text

    # ------------------------------------------------------------------
    # Locale iteration  (EN / NL)
    # ------------------------------------------------------------------

    def iter_locales(self):
        """Yield ``(locale_code, labels_dict, suffix)`` for each locale.

        *suffix* is ``""`` for English and ``"_NL"`` for Dutch.
        Override this if your example needs a different locale order.
        """
        texts = self.locale_text
        for locale, labels in (("en", texts["en"]),
                               ("nl", texts["nl"])):
            yield locale, labels, "" if locale == "en" else "_NL"

    # ------------------------------------------------------------------
    # Figure creation
    # ------------------------------------------------------------------

    def panel_figsize(self, panel: str) -> tuple[float, float]:
        """Return the figure size for *panel*, with per-panel override support."""
        return self.config.panel_figsize(panel)

    def create_figure(self, nrows: int = 1, ncols: int = 1,
                      figsize: tuple[float, float] | None = None):
        """Create a styled ``(figure, axes)`` matching this example's config.

        Parameters
        ----------
        nrows, ncols
            Subplot grid dimensions (default 1×1).
        figsize
            Override the figure size. Falls back to ``config.figsize`` or
            ``config.panel_figsize(panel)`` when *panel* is given.
        """
        figsize = figsize or self.config.figsize
        fig, axs = plt.subplots(nrows, ncols, figsize=figsize,
                                facecolor=BITROOT_PALETTE["surface"])
        if nrows * ncols == 1:
            axs.set_facecolor(BITROOT_PALETTE["surface"])
        else:
            for ax in axs.flat:
                ax.set_facecolor(BITROOT_PALETTE["surface"])
        return fig, axs

    # ------------------------------------------------------------------
    # Styling helper
    # ------------------------------------------------------------------

    def resolve_color(self, semantic: str) -> str:
        """Resolve a semantic colour name from the config to a hex string.

        Looks up ``config.colors[semantic]``; if no mapping exists, falls
        back to treating *semantic* itself as a palette key or
        tint/shade expression (e.g. ``"primary@tint(0.8)"``).

        Colour expressions are resolved via ``CCPlots.config.palette.resolve_palette_key``.
        """
        key_spec: str
        if self.config.colors and semantic in self.config.colors:
            key_spec = self.config.colors[semantic]
        else:
            key_spec = semantic
        return resolve_palette_key(key_spec)

    def apply_style(self, ax, **kwargs):
        """Apply the Bitroot theme to *ax* (proxies ``apply_bitroot_style``)."""
        return apply_bitroot_style(ax, **kwargs)

    # ------------------------------------------------------------------
    # Label styling
    # ------------------------------------------------------------------

    @property
    def text_color(self) -> str:
        """Convenience shortcut for ``BITROOT_PALETTE['on-surface']``."""
        return BITROOT_PALETTE["on-surface"]

    def text_color_for_background(self, bg_color: str, *, large: bool = False) -> str:
        """Return ``text`` or ``white`` — whichever gives better WCAG AA
        contrast against *bg_color*.

        Parameters
        ----------
        bg_color : str
            Background colour (hex, palette key, or ``@tint``/``@shade`` expression).
        large : bool
            Pass ``True`` for text ≥24 px or ≥18.66 px bold (3:1 threshold).
        """
        return contrasting_text_color(bg_color, large=large)

    def apply_labels(self, ax, *,
                     title: str | None = None,
                     xlabel: str | None = None,
                     ylabel: str | None = None,
                     title_size: int = 16,
                     label_size: int = 14,
                     color: str | None = None,
                     bg_color: str | None = None):
        """Set title / axis labels with Bitroot-consistent styling in one call.

        Text colour is resolved in this order:
            1. *color* — explicit override
            2. *bg_color* — auto-select ``text`` or ``white`` for WCAG AA
            3. ``self.text_color`` — default dark text

        Use *bg_color* when the labels sit on a coloured or dark
        background (e.g. inside a heatmap cell or filled patch).
        """
        if color is not None:
            c = color
        elif bg_color is not None:
            c = self.text_color_for_background(bg_color, large=(title_size >= 24 or label_size >= 18.66))
        else:
            c = self.text_color
        if title is not None:
            ax.set_title(title, fontsize=title_size, color=c, pad=10)
        if xlabel is not None:
            ax.set_xlabel(xlabel, fontsize=label_size, color=c)
        if ylabel is not None:
            ax.set_ylabel(ylabel, fontsize=label_size, color=c)

    # ------------------------------------------------------------------
    # Output helpers
    # ------------------------------------------------------------------

    def resolve_output(self, panel: str = "default", **fmt_args: Any) -> str:
        """Build the output filename from the config's pattern for *panel*."""
        return self.config.resolve_output(panel, **fmt_args)

    def save_figure(self, fig, panel: str = "default", **fmt_args: Any):
        """Save *fig* using the configured output pattern and close it.

        The filename is built from ``config.output_files[panel]`` by
        formatting with *fmt_args* (which must include ``suffix``).
        """
        fname = self.resolve_output(panel, **fmt_args)
        fig.savefig(output_path(fname),
                    bbox_inches="tight", pad_inches=0.1,
                    dpi=self.config.dpi)
        plt.close(fig)

    # ------------------------------------------------------------------
    # Required entry point
    # ------------------------------------------------------------------

    @abstractmethod
    def main(self) -> None:
        """Generate the plot(s) for this example."""

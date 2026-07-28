"""
``CCPlots.PlotExample`` — Abstract base class for all example plots.

Subclasses must define:
    - ``CONFIG_KEY`` (str) — matches the JSON filename in ``plot_configs/``
    - ``TEXT_BY_LOCALE`` (dict) — *optional fallback* locale text labels
      (already overridden when the JSON config contains a ``text`` section)
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
    load_example_config,
    output_path,
)


class PlotExample(ABC):

    # --- Must be overridden by every concrete subclass ---
    CONFIG_KEY: str = ""
    TEXT_BY_LOCALE: dict[str, dict[str, Any]] = {}

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
        """Locale text from the JSON config, or ``TEXT_BY_LOCALE`` as fallback."""
        if self.config.text is not None:
            return self.config.text
        return self.TEXT_BY_LOCALE

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
                                facecolor=BITROOT_PALETTE["background"])
        if nrows * ncols == 1:
            axs.set_facecolor(BITROOT_PALETTE["background"])
        else:
            for ax in axs.flat:
                ax.set_facecolor(BITROOT_PALETTE["background"])
        return fig, axs

    # ------------------------------------------------------------------
    # Styling helper
    # ------------------------------------------------------------------

    def resolve_color(self, semantic: str) -> str:
        """Resolve a semantic colour name from the config to a hex string.

        Looks up ``config.colors[semantic]``, then resolves it against
        ``BITROOT_PALETTE``. Falls back to treating *semantic* itself as
        a palette key, then as a literal hex string.
        """
        key: str
        if self.config.colors and semantic in self.config.colors:
            key = self.config.colors[semantic]
        else:
            key = semantic
        return BITROOT_PALETTE.get(key, key)

    def apply_style(self, ax, **kwargs):
        """Apply the Bitroot theme to *ax* (proxies ``apply_bitroot_style``)."""
        return apply_bitroot_style(ax, **kwargs)

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

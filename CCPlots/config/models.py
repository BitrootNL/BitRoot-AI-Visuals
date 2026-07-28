"""
``CCPlots.config.models`` — Typed schema for per-plot configuration.

**What this controls:**
- ``ExampleConfig`` — a frozen dataclass that each JSON plot config is validated
  against. Every per-plot config in ``CCPlots/plot_configs/*.json`` must conform
  to this schema.
- ``load_config_from_json()`` — low-level function that reads a JSON file path
  and returns an ``ExampleConfig`` instance with full validation.

**Scope: global.** The schema applies to every per-plot JSON config.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ExampleConfig:
    """Schema for a per-example plot configuration loaded from JSON.

    Fields
    ------
    key : str
        Unique identifier matching the JSON filename (e.g. ``"perceptron"``).
    output_files : dict[str, str]
        Mapping from logical panel name to filename pattern. Patterns may
        contain ``{suffix}`` (``""`` or ``"_NL"``) and other format placeholders.
    figsize : tuple[int, int]
        Default figure dimensions ``(width, height)`` in inches.
    dpi : int
        Output resolution. Defaults to ``100``.
    description : str or None
        Human-readable explanation of what this config controls (display only).
    params : dict or None
        Optional constructor parameters for the example class (e.g. ``n_clusters``).
    run : dict or None
        Optional run-time parameters (e.g. ``n_cities`` values to iterate over).
    panel_figsizes : dict[str, list[int]] or None
        Per-panel figure-size overrides. Falls back to ``figsize`` when absent.
    text : dict[str, dict[str, Any]] or None
        Locale-specific text labels. Keys are locale codes (``"en"``, ``"nl"``);
        values are dicts of label keys to text values.
    colors : dict[str, str] or None
        Semantic colour assignments mapping a role name (e.g. ``"line"``,
        ``"fill"``) to a ``BITROOT_PALETTE`` key or hex string.
    """

    key: str
    output_files: dict[str, str]
    figsize: tuple[float, float]
    dpi: int = 100
    description: str | None = None
    params: dict[str, Any] | None = None
    run: dict[str, Any] | None = None
    panel_figsizes: dict[str, list[int]] | None = None
    text: dict[str, dict[str, Any]] | None = None
    colors: dict[str, str] | None = None

    def panel_figsize(self, panel: str) -> tuple[float, float]:
        """Return the figure size for *panel*, with override support.

        If ``panel_figsizes[panel]`` exists, returns that; otherwise
        returns the default ``figsize``.
        """
        if self.panel_figsizes and panel in self.panel_figsizes:
            raw = self.panel_figsizes[panel]
            return (float(raw[0]), float(raw[1]))
        return self.figsize

    def resolve_output(self, panel: str, **fmt_args: Any) -> str:
        """Format the output filename pattern for *panel* with *fmt_args*.

        Example
        -------
        ``cfg.resolve_output("default", suffix="")``
        returns ``"perceptron_schematic.png"``.
        """
        pattern = self.output_files[panel]
        return pattern.format(**fmt_args)


def _coerce_figsize(raw: Any) -> tuple[float, float]:
    if isinstance(raw, (list, tuple)) and len(raw) == 2:
        return (float(raw[0]), float(raw[1]))
    raise TypeError(f"figsize must be a 2-element sequence, got {raw!r}")


def load_config_from_json(path: str) -> ExampleConfig:
    """Load, validate, and return an ``ExampleConfig`` from a JSON file.

    Raises
    ------
    FileNotFoundError
        If *path* does not exist.
    TypeError / ValueError
        If the JSON content does not match the expected schema.
    """
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Config file not found: {path}")

    with open(path, encoding="utf-8") as f:
        raw = json.load(f)

    if not isinstance(raw, dict):
        raise TypeError(f"Expected a JSON object in {path}, got {type(raw).__name__}")

    missing = [k for k in ("key", "output_files", "figsize") if k not in raw]
    if missing:
        raise ValueError(f"Missing required fields {missing} in {path}")

    figsize = _coerce_figsize(raw["figsize"])

    return ExampleConfig(
        key=raw["key"],
        output_files=raw["output_files"],
        figsize=figsize,
        dpi=raw.get("dpi", 100),
        description=raw.get("description"),
        params=raw.get("params"),
        run=raw.get("run"),
        panel_figsizes=raw.get("panel_figsizes"),
        text=raw.get("text"),
        colors=raw.get("colors"),
    )

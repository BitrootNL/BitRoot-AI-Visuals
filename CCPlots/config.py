"""Backward-compatible re-exports for the refactored ``config/`` package.

All public names are now defined in ``CCPlots.config`` (a package).
This module exists only so that existing imports from ``CCPlots.config``
continue to work without changes.
"""
from CCPlots.config import (  # noqa: F401
    BITROOT_PALETTE,
    OUTPUT_PATH,
    ExampleConfig,
    apply_bitroot_style,
    darken_color,
    load_example_config,
    output_path,
    probability_color,
)

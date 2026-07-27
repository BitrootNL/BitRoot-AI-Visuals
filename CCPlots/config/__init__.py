"""
``CCPlots.config`` — General configuration system for the CCPlots library.

This package provides three categories of configuration:

**1. Visual styling (palette)**
   ``BITROOT_PALETTE`` — shared colour reference for all plots.
   ``apply_bitroot_style()`` — applies the Bitroot theme to a matplotlib Axes.
   ``darken_color()`` / ``probability_color()`` — colour derivation helpers.

**2. Output paths**
   ``OUTPUT_PATH`` — root directory where all generated plots are saved.
   ``output_path()`` — resolves a relative filename to an absolute writable path.

**3. Per-plot configuration loading**
   ``ExampleConfig`` — validated dataclass that each plot's JSON config maps to.
   ``load_example_config()`` — loads a JSON config from ``CCPlots/plot_configs/``
   by a short key (e.g. ``"perceptron"``).

   *The actual per-plot JSON files live in ``CCPlots/plot_configs/``, NOT in this
   package. See that directory for per-example settings (output filenames, figure
   sizes, DPI, run parameters).*
"""

from .palette import (
    BITROOT_PALETTE,
    apply_bitroot_style,
    darken_color,
    probability_color,
)
from .paths import OUTPUT_PATH, output_path
from .loader import load_example_config
from .models import ExampleConfig

__all__ = [
    "BITROOT_PALETTE",
    "OUTPUT_PATH",
    "ExampleConfig",
    "apply_bitroot_style",
    "darken_color",
    "load_example_config",
    "output_path",
    "probability_color",
]

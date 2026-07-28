"""
``CCPlots.config.paths`` — Output path resolution for generated plots.

**What this controls:**
- ``OUTPUT_PATH`` — the root directory where ``CCPlots`` saves every generated
  image and animation (default: ``<project-root>/plots/``).
- ``output_path()`` — the canonical way to build a writable absolute path from a
  relative filename. Creates parent directories as needed.

**Scope: global.** All examples share the same output root.
Per-example filenames are configured in ``CCPlots/plot_configs/*.json``.
"""

import os

_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

OUTPUT_PATH = os.path.join(_PROJECT_ROOT, "plot-output") + os.sep
os.makedirs(OUTPUT_PATH, exist_ok=True)


def output_path(filename: str) -> str:
    """Return a writable absolute path under ``OUTPUT_PATH`` for the given filename.

    Creates any parent subdirectories that do not yet exist.
    """
    full_path = os.path.join(OUTPUT_PATH, filename)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    return full_path

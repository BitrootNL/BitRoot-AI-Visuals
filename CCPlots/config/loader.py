"""
``CCPlots.config.loader`` — Loads per-plot configuration from JSON files.

**What this controls:**
- Which per-plot JSON file is loaded when ``load_example_config("key")`` is called.
- A process-wide cache (``_EXAMPLE_CONFIG_REGISTRY``) so each file is parsed once.

**How it finds the JSON files:**
All per-plot configs live in ``CCPlots/plot_configs/`` (one ``.json`` file per
example). This directory is **not** part of the ``CCPlots.config`` system package
— it holds data files, not code.
"""

import os

from .models import ExampleConfig, load_config_from_json

# Path to the per-plot JSON configs (data files, not part of this code package).
_PLOT_CONFIG_DIR = os.path.join(os.path.dirname(__file__), "..", "plot_configs")
_EXAMPLE_CONFIG_REGISTRY: dict[str, ExampleConfig] = {}


def load_example_config(key: str) -> ExampleConfig:
    """Load a per-example config JSON by its key (e.g. ``"perceptron"``).

    Results are cached so each file is parsed only once per process.
    """
    cached = _EXAMPLE_CONFIG_REGISTRY.get(key)
    if cached is not None:
        return cached

    json_path = os.path.join(_PLOT_CONFIG_DIR, f"{key}.json")
    cfg = load_config_from_json(json_path)
    _EXAMPLE_CONFIG_REGISTRY[key] = cfg
    return cfg

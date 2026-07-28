"""
``CCPlots.config.mermaid_theme`` — Bitroot Mermaid theme from ``bitroot.json``.

Provides ``get_mermaid_theme()`` returning a ``mmdc``-compatible theme dict,
and ``write_mermaid_config()`` to write it to disk.

The theme variable mapping follows ``.github/instructions/DESIGN.md``.
"""

from __future__ import annotations

import json
import os
from typing import Any

from .palette import BITROOT_PALETTE


def get_mermaid_theme() -> dict[str, Any]:
    """Return a Mermaid CLI theme dict derived from the Bitroot palette.

    Mapping follows the DESIGN.md Mermaid config:

    =========================  ===============  =========================
    Mermaid variable           Bitroot key      Role
    =========================  ===============  =========================
    ``background``             ``surface``      Page background
    ``primaryColor``           ``surface-elev`` Default node fill
    ``primaryTextColor``       ``on-surface``   Node label text
    ``primaryBorderColor``     ``primary``      Node border (brand accent)
    ``lineColor``              ``secondary``    Connector lines / arrows
    ``secondaryColor``         ``tertiary``     Secondary node fill
    ``secondaryTextColor``     ``on-surface``   Secondary node label text
    ``secondaryBorderColor``   ``tertiary``     Secondary node border
    ``tertiaryColor``          ``surface``      Tertiary node fill
    ``tertiaryTextColor``      ``on-surface-muted`` Tertiary node text
    ``tertiaryBorderColor``    ``border``       Tertiary node border
    ``fontFamily``             —                ``Inter, system-ui, sans-serif``
    ``fontSize``               —                ``16px``
    ``edgeLabelBackground``    ``white``        Edge label background
    =========================  ===============  =========================
    """
    p = BITROOT_PALETTE
    return {
        "theme": "base",
        "themeVariables": {
            "background": p["surface"],
            "primaryColor": p["surface-elev"],
            "primaryTextColor": p["on-surface"],
            "primaryBorderColor": p["primary"],
            "lineColor": p["secondary"],
            "secondaryColor": p["tertiary"],
            "secondaryTextColor": p["on-surface"],
            "secondaryBorderColor": p["tertiary"],
            "tertiaryColor": p["surface"],
            "tertiaryTextColor": p["on-surface-muted"],
            "tertiaryBorderColor": p["border"],
            "fontFamily": "Inter, system-ui, sans-serif",
            "fontSize": "16px",
            "edgeLabelBackground": p["white"],
        },
    }


def write_mermaid_config(path: str) -> str:
    """Write the Mermaid theme config to *path* and return it."""
    theme = get_mermaid_theme()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(theme, f, indent=2)
    return path

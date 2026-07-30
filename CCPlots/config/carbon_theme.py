"""
``CCPlots.config.carbon_theme`` — Bitroot Carbon (code snippet) theme.

Provides ``get_carbon_config()`` returning a ``carbon-now``-compatible config
dict suitable for ``--config`` or ``--settings``.
"""

from __future__ import annotations

from typing import Any

from .palette import BITROOT_PALETTE, shade_color


def get_carbon_config() -> dict[str, Any]:
    """Return a carbon-now-cli config dict derived from the Bitroot palette.

    The syntax-highlighting colours are mapped from the Bitroot design
    system to provide a clean, readable code snippet appearance.

    Brand (beetroot) is used sparingly — only for class-name tokens.
    Base text carries a subtle primary (cyan) undertone via a dark shade.
    Numbers use primary for visibility without overusing brand.
    """
    p = BITROOT_PALETTE
    mono_font = "JetBrains Mono, IBM Plex Mono, ui-monospace, Menlo, monospace"

    return {
        "theme": "one-light",
        "backgroundColor": p["surface-elev"],
        "windowTheme": "none",
        "fontFamily": mono_font,
        "fontSize": 14,
        "lineHeight": 1.7,
        "paddingHorizontal": 32,
        "paddingVertical": 32,
        "watermark": False,
        "dropShadow": False,
        "lineNumbers": True,
        "exportSize": "2x",
        "customColors": {
            "backgroundColor": p["surface-elev"],
            "textColor": shade_color(p["primary"], 0.25),
            "lineNumberColor": p["on-surface-disabled"],
            "stringColor": p["success"],
            "keywordColor": p["primary"],
            "functionColor": p["secondary"],
            "numberColor": p["primary"],
            "commentColor": p["on-surface-disabled"],
            "variableColor": shade_color(p["primary"], 0.25),
            "operatorColor": p["on-surface-muted"],
            "typeColor": p["tertiary"],
            "punctuationColor": p["on-surface-muted"],
            "invalidColor": p["error"],
            "builtInColor": shade_color(p["primary"], 0.7),
            "classNameColor": p["brand"],
            "propertyColor": p["tertiary"],
            "tagColor": p["primary"],
            "attributeColor": p["secondary"],
        },
    }

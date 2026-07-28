"""
Render all Mermaid diagrams in ``mermaid/`` via the Mermaid CLI (mmdc).

Each ``.md`` source file containing a `` ```mermaid `` code block is
rendered to SVG and PNG using the Bitroot theme derived from
``CCPlots/config/bitroot.json``.

Usage
-----
    python generate_mermaid.py

Requires ``@mermaid-js/mermaid-cli`` (install via ``npm install``).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile

from CCPlots.config.mermaid_theme import get_mermaid_theme

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
MERMAID_DIR = os.path.join(PROJECT_ROOT, "mermaid")

# Regex to extract content from a ```mermaid ... ``` code block.
_MERMAID_BLOCK_RE = re.compile(
    r"```mermaid\s*\n(.*?)```",
    re.DOTALL,
)


def _find_sources() -> list[str]:
    """Return paths of every ``.md`` file in ``mermaid/`` with a mermaid code block."""
    sources: list[str] = []
    for entry in sorted(os.listdir(MERMAID_DIR)):
        if not entry.lower().endswith(".md"):
            continue
        path = os.path.join(MERMAID_DIR, entry)
        with open(path, encoding="utf-8") as f:
            if "```mermaid" in f.read():
                sources.append(path)
    return sources


def _extract_mermaid(source_path: str) -> str:
    """Extract the raw Mermaid syntax from a Markdown code block.

    Returns empty string if no fenced mermaid block is found.
    """
    with open(source_path, encoding="utf-8") as f:
        content = f.read()
    m = _MERMAID_BLOCK_RE.search(content)
    return m.group(1).strip() if m else ""


def _find_mmdc() -> str:
    """Return the path to the mmdc binary, or raise ``FileNotFoundError``."""
    bin_dir = os.path.join(PROJECT_ROOT, "node_modules", ".bin")
    if sys.platform == "win32":
        candidate = os.path.join(bin_dir, "mmdc.cmd")
        if os.path.isfile(candidate):
            return candidate
    candidate = os.path.join(bin_dir, "mmdc")
    if os.path.isfile(candidate):
        return candidate
    raise FileNotFoundError(
        "mmdc not found — run ``npm install`` to install "
        "@mermaid-js/mermaid-cli"
    )


def _render_one(source_path: str, config_path: str, mmdc_path: str, bg: str) -> tuple[str, str]:
    """Render a single Mermaid source file to SVG and PNG.

    Extracts the mermaid syntax from the Markdown code block, writes it to
    a temporary ``.mmd`` file, renders via mmdc, then cleans up.
    """
    stem = os.path.splitext(os.path.basename(source_path))[0]
    svg_path = os.path.join(MERMAID_DIR, f"{stem}.svg")
    png_path = os.path.join(MERMAID_DIR, f"{stem}.png")

    raw = _extract_mermaid(source_path)
    if not raw:
        msg = f"No mermaid code block found in {source_path}"
        raise ValueError(msg)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".mmd", delete=False, encoding="utf-8",
    ) as f:
        f.write(raw)
        mmd_path = f.name

    try:
        for out_path in (svg_path, png_path):
            subprocess.run(
                [mmdc_path, "-i", mmd_path, "-o", out_path,
                 "-c", config_path, "-b", bg],
                check=True, capture_output=True, text=True,
            )
    finally:
        os.unlink(mmd_path)

    return svg_path, png_path


def main() -> None:
    sources = _find_sources()
    if not sources:
        print("No Mermaid source files found in mermaid/")
        return

    theme = get_mermaid_theme()
    bg = theme["themeVariables"]["background"]

    try:
        mmdc_path = _find_mmdc()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8",
    ) as f:
        json.dump(theme, f, indent=2)
        config_path = f.name

    print(f"Rendering {len(sources)} Mermaid diagram(s)...")
    try:
        for src in sources:
            name = os.path.basename(src)
            print(f"  {name}")
            svg, png = _render_one(src, config_path, mmdc_path, bg)
            print(f"    SVG -> {os.path.basename(svg)}")
            print(f"    PNG -> {os.path.basename(png)}")
    finally:
        os.unlink(config_path)

    print("Done.")


if __name__ == "__main__":
    main()

"""
Render all code snippet source files in ``code-snippets/`` via carbon-now-cli.

Each ``.py`` file is rendered to ``.py.png`` in the same directory, using the
Bitroot syntax-highlighting theme derived from ``CCPlots/config/bitroot.json``.

Usage
-----
    python generate_snippets.py

Requires ``carbon-now-cli`` (install via ``npm install``).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

from CCPlots.config.carbon_theme import get_carbon_config

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
SNIPPETS_DIR = os.path.join(PROJECT_ROOT, "code-snippets")
SNIPPETS_OUTPUT_DIR = os.path.join(PROJECT_ROOT, "snippet-output")


def _find_sources() -> list[str]:
    """Return paths of every ``.py`` file under ``code-snippets/``."""
    sources: list[str] = []
    for root, _dirs, files in os.walk(SNIPPETS_DIR):
        for f in sorted(files):
            if f.endswith(".py"):
                sources.append(os.path.join(root, f))
    return sources


def _find_carbon_now() -> str:
    """Return the path to the carbon-now binary, or raise ``FileNotFoundError``."""
    bin_dir = os.path.join(PROJECT_ROOT, "node_modules", ".bin")
    if sys.platform == "win32":
        candidate = os.path.join(bin_dir, "carbon-now.cmd")
        if os.path.isfile(candidate):
            return candidate
    candidate = os.path.join(bin_dir, "carbon-now")
    if os.path.isfile(candidate):
        return candidate
    raise FileNotFoundError(
        "carbon-now not found — run ``npm install`` to install "
        "carbon-now-cli"
    )


def _render_one(source_path: str, carbon_path: str, config_path: str) -> str:
    """Render *source_path* to ``.py.png`` under ``SNIPPETS_OUTPUT_DIR``.

    Returns the output image path.
    """
    rel = os.path.relpath(os.path.dirname(source_path), SNIPPETS_DIR)
    out_dir = os.path.join(SNIPPETS_OUTPUT_DIR, rel)
    os.makedirs(out_dir, exist_ok=True)

    src_stem = os.path.basename(source_path)          # e.g. sklearn_clustering.py

    subprocess.run(
        [carbon_path, source_path,
         "--save-to", out_dir,
         "--save-as", src_stem,
         "--config", config_path,
         "--skip-display"],
        check=True, capture_output=True, text=True,
    )
    return os.path.join(out_dir, f"{src_stem}.png")


def main() -> None:
    sources = _find_sources()
    if not sources:
        print("No .py source files found in code-snippets/")
        return

    try:
        carbon_path = _find_carbon_now()
    except FileNotFoundError as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

    config = get_carbon_config()

    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, encoding="utf-8",
    ) as f:
        json.dump(config, f, indent=2)
        config_path = f.name

    print(f"Rendering {len(sources)} code snippet(s)...")
    ok = 0
    failed: list[str] = []
    try:
        for src in sources:
            rel = os.path.relpath(src, SNIPPETS_DIR)
            print(f"  {rel}")
            try:
                out = _render_one(src, carbon_path, config_path)
                print(f"    -> {os.path.basename(out)}")
                ok += 1
            except subprocess.CalledProcessError as exc:
                print(f"    FAILED (exit {exc.returncode})")
                failed.append(rel)
    finally:
        os.unlink(config_path)

    if failed:
        print(f"\n{ok} succeeded, {len(failed)} failed:")
        for f in failed:
            print(f"  - {f}")
        sys.exit(1)
    else:
        print(f"\nAll {ok} snippet(s) rendered successfully.")


if __name__ == "__main__":
    main()

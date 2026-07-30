# Plotting Style Instructions

## Shared design foundation
All visuals in this repository share ONE source of truth: `CCPlots/config/bitroot.json`.
Every colour, spacing token, and typography rule originates there. Do NOT hard-code
hex values in Python code, JSON configs, or Mermaid sources — always reference
palette keys (e.g. `"primary"`, `"surface-elev"`) and use `resolve_palette_key()`,
`tint_color()`, or `shade_color()` to derive variants.

Three theme modules consume `bitroot.json` and expose it to their respective output
pipelines:

| Module (`CCPlots/config/`) | Purpose | Consumed by |
|---|---|---|
| `palette.py` | `BITROOT_PALETTE` dict, `apply_bitroot_style()`, colour derivation | `generate_plots.py` (matplotlib) |
| `mermaid_theme.py` | `get_mermaid_theme()` → mmdc-compatible JSON | `generate_mermaid.py` (mmdc CLI) |
| `carbon_theme.py` | `get_carbon_config()` → carbon-now-compatible JSON | `generate_snippets.py` (carbon-now CLI) |

To change a colour, edit `CCPlots/config/bitroot.json` — all three output pipelines
pick it up automatically. Never patch colours in theme modules alone.

## Project context
- This repository generates teaching-focused plots for AI and machine learning concepts.
- The visual system should stay calm, readable, and educational rather than overly dramatic.
- Every plot that supports text labels produces an English (EN) and Dutch (NL) version.
  The EN filename has no suffix; the NL filename ends with `_NL`.

## Design source of truth
- Follow the palette and guidance in `colour_reference.md`.
- The palette is defined in `CCPlots/config/palette.py` as the `BITROOT_PALETTE` dict.
- Use the Bitroot palette consistently for chart series, backgrounds, text, and gridlines.
- Prefer shades of the primary colour to provide calmness. Scale the lightness along with values where this makes sense.
- Use the secondary colour for accents.
- Use the tertiary colour sparingly as it has poor visibility. It does work well for data points, where a primary-coloured line is plotted.
- Only use success, warning and error colors when they are directly relevant to the example (e.g. a confusion matrix with real costs, or a performance metric). Do not use them for general categorical coloring or decoration.
- Use highlight colors sparingly for emphasis only.

## Styling rules
- Keep backgrounds light and clean.
- Use dark text for readability and contrast.
- Avoid overly saturated or high-energy colors in core chart fills.
- Use softer, muted shades for supporting regions when the chart needs calm visual hierarchy.
- Maintain WCAG AA-friendly contrast for labels and important elements.
- When multiple related shades are needed, derive them from the Bitroot palette and keep them consistent across examples rather than introducing ad hoc colors.
- For value-driven encodings such as probability, confidence, or intensity, use a monotonic gradient of primary-based shades where larger values appear darker.
- Grid colour is set globally by `apply_bitroot_style()`. Do NOT set grid colour per-example.

## Colour derivation
- Use `tint_color(color, amount)` to lighten toward white: `new = current + ((255 − current) × amount)`.
- Use `shade_color(color, amount)` to darken toward black: `new = current × amount`.
- `darken_color()` is deprecated — use `shade_color()` instead.
- All RGB values are rounded to the nearest whole number (.5 rounds up).
- In JSON configs, use `"primary@tint(0.8)"` or `"secondary@shade(0.6)"` expressions to derive colours inline.

## Configuration architecture

### System package: `CCPlots/config`
| Module | Responsibility |
|---|---|
| `palette.py` | `BITROOT_PALETTE`, `tint_color`, `shade_color`, `resolve_palette_key()`, `apply_bitroot_style()` |
| `paths.py` | `OUTPUT_PATH`, `output_path()` |
| `models.py` | `ExampleConfig` dataclass — schema for per-example JSON configs |
| `loader.py` | `load_example_config(key)` — loads and caches JSON configs |

The old `CCPlots/config.py` is a backward-compatible shim. New code should import from `CCPlots.config` (the package) directly.

### Per-example configs: `CCPlots/plot_configs/`
Each `.json` file contains:
- `key` — unique identifier matching the filename stem
- `output_files` — filename patterns with `{suffix}` placeholder
- `figsize`, `dpi` — figure dimensions and resolution
- `text` — locale-specific labels (`en` / `nl`), replaces the old `TEXT_BY_LOCALE` class attribute
- `colors` — semantic colour roles mapped to palette keys or `@tint`/`@shade` expressions
- `params` — optional constructor parameters (e.g. `n_clusters`)
- `run` — optional runtime parameters (e.g. `n_cities`)
- `panel_figsizes` — optional per-panel figure-size overrides

To change a label or colour, edit the JSON — no Python code changes needed.

### Global random state
A single seed `GLOBAL_RANDOM_STATE = 42` (`CCPlots/config/__init__.py`) is used by all examples for numpy, sklearn, and Python random calls to guarantee reproducible output.

## Implementation preferences
- Centralize styling in `CCPlots/config` when possible.
- Reuse shared helper functions from `PlotExample` instead of hard-coding colour values in every example.
- Every implementation is a subclass of `PlotExample` with a `CONFIG_KEY`.
- Use the base class helpers: `self.create_figure()`, `self.apply_style()`, `self.apply_labels()`, `self.save_figure()`, `self.iter_locales()`.
- Use `self.resolve_color(semantic)` for any colour that may change per example. Add the mapping to the JSON config's `colors` section.
- Use `self.text_color` instead of `BITROOT_PALETTE['text']` for axis labels, titles, and annotation text.
- Use `BITROOT_PALETTE` directly only for structural colours (background, grid) where per-example configurability provides no value.
- Grid colour is set globally by `apply_style()` → `apply_bitroot_style()`. Never override it per-example.
- For bar or categorical gradients, use `LinearSegmentedColormap.from_list()` with config-driven endpoints, not the legacy `probability_color()` function.
- Preserve existing output filenames and plotting behavior unless a change is explicitly requested.
- Prefer incremental, low-risk updates that keep the examples working.
- **Plots are auto-overwritten:** Never manually delete plot files — each run overwrites them automatically. This avoids accidentally losing reference output files.
- **Localization:** Every plot that supports Dutch (NL) must also produce an English (EN) counterpart. Text labels are stored in each plot's JSON config under a `text` key with locale pairs `("en", "nl")`. Append `_NL` to the NL output filename; the EN filename has no suffix.
- **Avoid `tight_layout`:** Do not call `fig.tight_layout()` or `plt.tight_layout()` — it can misalign axes, especially with multi-locale plots. Use `bbox_inches='tight'` in `savefig` instead if padding adjustment is needed.

## Example architecture
1. Add a JSON config file to `CCPlots/plot_configs/` with your config key.
2. Create a class inheriting from `PlotExample` with `CONFIG_KEY = "your_key"`.
3. Implement `main()` using `self.iter_locales()`, `self.create_figure()`, `self.apply_labels()`, `self.save_figure()`.
4. Add locale text to the JSON `text` section.
5. Use `self.resolve_color()` for any colour that should be configurable, and add the keys to the JSON `colors` section.

## Example-specific guidance
- For paired views that show the same dataset with and without binning, use the primary colour for both panels.
- For charts that cannot be heavily styled, such as decision tree plots, keep the surrounding figure and axis styling aligned with the Bitroot palette and avoid forcing custom series colours.
- Prefer shades of the primary colour for most series and use the secondary colour as a single accent.
- Keep general chart styling free from warning yellow and avoid introducing extra colours when a single hue is sufficient.
- For animations, keep the animated line or marker colour in the primary hue; use secondary only as a contrast accent when it improves readability.
- For plots where a line and points need separation, make the points slightly darker or more saturated than the line.
- For growth or progression charts, use the same hue with different opacities or shades rather than mixing green and cyan.
- For bar or categorical plots that need multiple related colours, use a tonal progression derived from the same hue rather than repeating the exact same colour.
- For layout-sensitive examples, make sure titles, axis labels, and tick labels have enough breathing room and avoid clipping during save/export.

## Verification
- After making style changes, regenerate the relevant example plot and confirm the output file is created successfully.
- If a change affects multiple examples, verify at least one representative plot and the overall plotting workflow.
- Run `python generate_plots.py` to regenerate all plots.

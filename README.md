# BitRoot AI Visuals

Teaching-focused plots and learning materials for AI and machine learning courses.

## About

This repository generates plots, diagrams, and code snippets used in AI course
materials. All visuals are generated programmatically and styled from the
[Bitroot design system](CCPlots/config/bitroot.json).

## Contents

- [Python Plots](#python-plots) — matplotlib plots via CCPlots
- [Mermaid Diagrams](#mermaid-diagrams) — flowcharts via mmdc (`mermaid/` → `mermaid-output/`)
- [Code Snippets](#code-snippets) — syntax-highlighted code via carbon-now-cli (`code-snippets/` → `snippet-output/`)
- [Plot Showcase](#plot-showcase)

## Python Plots

The `CCPlots` module generates all plots in `plot-output/`.

1. Install dependencies: `pip install -r requirements.txt`
2. Regenerate all plots: `python generate_plots.py`
3. Or run a single example: `python -c "import CCPlots; CCPlots.<ClassName>().main()"` (see table below for class names)

Every example is a subclass of `PlotExample` (defined in `CCPlots/PlotExample.py`)
with a `CONFIG_KEY` that links it to its JSON config in `CCPlots/plot_configs/`.
All examples can be run via `generate_plots.py` uniformly.

### Configuration-driven

Each plot is configured by a JSON file in `CCPlots/plot_configs/`:
- Output filenames, figure size, DPI
- Locale-specific text labels (``text`` section)
- Semantic colour mappings (``colors`` section, optional)
- Plot-specific parameters (``params``, ``run`` sections)

To change a label or colour, edit the JSON — no Python code changes needed.

A global random seed (`GLOBAL_RANDOM_STATE = 42` in `CCPlots/config/`) is
used consistently by all examples for numpy, sklearn, and Python random calls.

### Localization

Every plot that supports text labels produces an English (EN) and Dutch (NL)
version. The EN filename has no suffix; the NL filename ends with `_NL`.
Text labels are stored in each plot's JSON config under a ``text`` key with
locale pairs `("en", "nl")`.

### Implementations

| Class | Config | Output |
|---|---|---|
| `Classification` | `classification.json` | `classification_decision_boundary.png`, `classification_confusion_matrix.png` |
| `ContinuousDiscrete` | `continuous_discrete.json` | `continuous_discrete.png` |
| `DecisionTree` | `decision_tree.json` | `decision_tree_iris.png` |
| `EmployeeAIAdoption` | `employee_ai_adoption.json` | `employee_ai_adoption.png` |
| `FraudDetection` | `fraud_detection.json` | `fraud_detection_boundary.png` |
| `KFolds` | `kfolds.json` | `kfold_validation.png` |
| `KMeans` | `kmeans.json` | `kmeans_animation_k3.gif`, `kmeans_clustering_k3.png` |
| `KNearest` | `knearest.json` | `knn_visualization_animation.gif` |
| `LLMPredict` | `llm_predict.json` | `llm_predict_next.png` |
| `LinearRegression` | `linear_regression.json` | `linear_regression_animation.gif` |
| `LogisticRegression` | `logistic_regression.json` | `logistic_regression_animation.gif` |
| `MSE` | `mse.json` | `mse_over_iterations.png` |
| `MSEZoom` | `mse_zoom.json` | `mse_zoom_iteration.png` |
| `MissingData` | `missing_data.json` | `missing_data_table.png` |
| `MultivariateRegression` | `multivariate_regression.json` | `multivariate_regression_animation.gif` |
| `NeuralNetSchematic` | `neural_net_schematic.json` | `neural_net_schematic.png` |
| `NeuralNetworkActivationFunctions` | `neural_network_activation_functions.json` | `neural_network_activation_functions.png` |
| `NeuralNetworkGrowth` | `neural_network_growth.json` | `neural_network_growth_line_log.png` |
| `NoisyData` | `noisy_data.json` | `noisy_data.png` |
| `NormalDistribution` | `normal_distribution.json` | `normal_distribution.png` |
| `OverfittingUnderfitting` | `overfitting_underfitting.json` | `overfitting_underfitting.png` |
| `Perceptron` | `perceptron.json` | `perceptron_schematic.png` |
| `Tokenization` | `tokenization.json` | `tokenization.png` |
| `TravelingSalesman` | `traveling_salesman.json` | `traveling_salesman_small_<n>_cities.png`, `traveling_salesman_large_<n>_cities.png` |

## Mermaid Diagrams

Source files (`.md`) live in `mermaid/`. Rendered SVG and PNG output is
written to `mermaid-output/`. Diagrams are styled with the Bitroot theme
derived from `bitroot.json` and rendered via the Mermaid CLI.

1. Install Node dependencies: `npm install`
2. Regenerate all diagrams: `python generate_mermaid.py`

| Source (`mermaid/`) | Locales | Outputs (`mermaid-output/`) |
|---|---|---|
| `eu_ai_act_classification.md` | EN | `{stem}.svg`, `{stem}.png` |
| `eu_ai_act_classification_NL.md` | NL | `{stem}.svg`, `{stem}.png` |
| `ml_algorithms_overview.md` | EN | `{stem}.svg`, `{stem}.png` |
| `ml_algorithms.md` | EN | `{stem}.svg`, `{stem}.png` |
| `scientific_method.md` | EN | `{stem}.svg`, `{stem}.png` |

## Code Snippets

Python source files (`.py`) live in `code-snippets/` organised by topic.
Rendered screenshots (`.py.png`) are written to `snippet-output/`
mirroring the same subdirectory structure. Snippets are styled with the
Bitroot syntax-highlighting theme and rendered via carbon-now-cli.

1. Install Node dependencies: `npm install`
2. Regenerate all snippets: `python generate_snippets.py`

| Source (`code-snippets/`) | Contents | Outputs (`snippet-output/`) |
|---|---|---|
| `algorithms/` | sklearn API examples | `algorithms/*.py.png` |
| `exercise_snippets/` | Starter code for exercises | `exercise_snippets/*.py.png` |
| `finetuning/` | Grid search / hyperparameter tuning | `finetuning/*.py.png` |
| `model_selection/` | LazyPredict comparison output | `model_selection/*.py.png` |
| `preprocessing/` | Data cleaning, binning, normalization, etc. | `preprocessing/*.py.png` |

## Styling

All visuals (plots and Mermaid diagrams) follow the **Bitroot** palette
defined in [`CCPlots/config/bitroot.json`](CCPlots/config/bitroot.json),
the single source of truth derived from the Bitroot design system.

| Token | Hex | Role |
|---|---|---|
| `primary` | `#269FBA` | Brand accent / node borders |
| `secondary` | `#5C78D9` | Connector lines / arrows |
| `tertiary` | `#A3D979` | Secondary node fills |
| `brand` | `#B1325D` | Emphatic accent (sparingly) |
| `surface` | `#F8FAFA` | Page / chart background |
| `on-surface` | `#2D3333` | Primary text colour |
| `on-surface-muted` | `#4D5C5C` | Secondary / muted text |
| `border` | `#D8E0E0` | Grid lines / borders |
| `white` | `#F2F2F5` | Card backgrounds / light contrast |

The palette is consumed by three theme modules — one per output type:

| Module | Config | Purpose |
|---|---|---|
| `CCPlots/config/palette.py` | `bitroot.json` | `BITROOT_PALETTE`, matplotlib styling, colour derivation |
| `CCPlots/config/mermaid_theme.py` | `bitroot.json` | `mmdc`-compatible theme for Mermaid diagrams |
| `CCPlots/config/carbon_theme.py` | `bitroot.json` | `carbon-now`-compatible theme for code snippets |

## Plot Showcase

![Linear Regression Animation](plot-output/linear_regression_animation.gif)
![Multivariate Regression Animation](plot-output/multivariate_regression_animation.gif)
![KMeans Clustering Animation](plot-output/kmeans_animation_k3.gif)
![KNN Regression Animation](plot-output/knn_visualization_animation.gif)
![Logistic Regression Animation](plot-output/logistic_regression_animation.gif)
![Classification](plot-output/classification_decision_boundary.png)
![K-Fold Validation](plot-output/kfold_validation.png)
![Overfitting vs Underfitting](plot-output/overfitting_underfitting.png)
![MSE Zoom](plot-output/mse_zoom_iteration.png)
![Neural Network Growth](plot-output/neural_network_growth_line_log.png)
![Activation Functions](plot-output/neural_network_activation_functions.png)
![Noisy Data](plot-output/noisy_data.png)
![Normal Distribution](plot-output/normal_distribution.png)
![Perceptron Schematic](plot-output/perceptron_schematic.png)
![Neural Network Schematic](plot-output/neural_net_schematic.png)
![Traveling Salesman](plot-output/traveling_salesman_small_4_cities.png)
![Decision Tree](plot-output/decision_tree_iris.png)

# Code Snippet Style Instructions

## Shared design foundation
All visuals in this repository share ONE source of truth: `CCPlots/config/bitroot.json`.
Code snippets use the Bitroot syntax-highlighting theme derived from `bitroot.json`
via `CCPlots/config/carbon_theme.py` and rendered by the `carbon-now-cli` Node package.

Do NOT modify syntax colours directly — edit `CCPlots/config/bitroot.json` and
regenerate. All three output pipelines (plots, mermaid, snippets) pick up the change.

## Theme architecture

| Layer | File | Role |
|---|---|---|
| Source of truth | `CCPlots/config/bitroot.json` | All hex values |
| Theme builder | `CCPlots/config/carbon_theme.py` | `get_carbon_config()` → carbon-now settings dict |
| Renderer | `generate_snippets.py` | Walks `code-snippets/`, renders via `carbon-now` CLI |

The carbon theme maps Bitroot tokens to syntax-highlighting roles:

| Token role | Bitroot key |
|---|---|
| Background | `surface-elev` |
| Text (base) | `primary@shade(0.25)` — dark cyan |
| Line numbers | `on-surface-disabled` |
| Strings | `success` |
| Keywords | `primary` |
| Functions | `secondary` |
| Numbers | `primary` |
| Comments | `on-surface-disabled` |
| Class names | `brand` (beet — used sparingly) |
| Types | `tertiary` |

## Directory & file conventions

| Location | Purpose |
|---|---|
| `code-snippets/<topic>/` | Source `.py` files, organised by topic |
| `snippet-output/<topic>/` | Rendered `.py.png` files (auto-generated) |

### Topic directories
Each subdirectory in `code-snippets/` covers one theme:
- `algorithms/` — sklearn, statsmodels API examples
- `exercise_snippets/` — starter code for exercises
- `finetuning/` — grid search / hyperparameter tuning
- `model_selection/` — model comparison (e.g. LazyPredict)
- `preprocessing/` — data cleaning, binning, normalization, encoding, etc.

Create new topic directories as needed. Choose a short, descriptive kebab-case name.

### File naming
- `snake_case_descriptive_name.py`
- The rendered output `snake_case_descriptive_name.py.png` is generated automatically.
- No EN/NL suffix — code is language-agnostic.

## Workflow for adding a new code snippet

1. Choose the topic directory under `code-snippets/`. Create one if it doesn't exist.
2. Write a `.py` file with:
   - A docstring header identifying the chapter and topic.
   - Clean, minimal code that demonstrates one concept.
   - Print statements for output where relevant.
3. Run `python generate_snippets.py` from the project root.
4. Verify the `.py.png` output appears under `snippet-output/`.

Example skeleton (`code-snippets/algorithms/sklearn_knn_classifier.py`):
```python
"""
sklearn_knn_classifier.py

Chapter: Algorithms
Topic: Supervised Learning, k-Nearest Neighbors classification
"""
from sklearn.neighbors import KNeighborsClassifier

# Example data
X = [[1, 2], [2, 3], [3, 1], [6, 5], [7, 7], [8, 6]]
y = [0, 0, 0, 1, 1, 1]

# Model
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X, y)

# Prediction
print(knn.predict([[5, 5]]))
```

## Content guidelines

### Code style
- Use 4-space indentation (PEP 8).
- Max line length ~72 characters to fit comfortably inside the carbon-now frame.
- Include imports explicitly — snippets should be self-contained.
- Prefer `print()` over `return` so the output is visible in the static image.
- Add a brief comment for non-obvious lines, but don't over-comment.

### Teaching focus
- Each snippet demonstrates exactly one concept or API pattern.
- Use simple, synthetic data (small lists, numpy arrays with few rows).
- Avoid long docstrings or verbose error handling — keep the signal-to-noise ratio high.
- The rendered image is used in slide decks and course materials. Aim for 15-30 lines
  of code so the image fits on one slide without scrolling.

### What NOT to do
- Don't add matplotlib/pyplot code — use the CCPlots pipeline for visualizations.
- Don't write to files — snippets should be pure computation + print.
- Don't use external data files unless the topic genuinely requires it (e.g. penguins
  dataset for train/test split). When you do, note the data source in the docstring.
- Don't add language-specific comments (`# NL: ...` / `# EN: ...`) — code is
  language-agnostic; textual explanations go in the course materials, not the snippet.

## Verification
- Run `python generate_snippets.py` to regenerate all snippets.
- Check the `.py.png` output file exists in `snippet-output/<topic>/`.
- Open the PNG and verify the rendering is clean: correct font (JetBrains Mono),
  no clipping, readable line numbers.
- If you added a new topic directory, update `README.md` in the code-snippets table.

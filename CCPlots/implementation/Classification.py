"""
Two-output classification example: a decision-boundary scatter plot and a
confusion matrix (with expanded TN / FP / FN / TP labels) for a diabetes
prediction task using logistic regression.

Figures
-------
- ``classification_decision_boundary.png`` / ``_NL.png`` — decision boundary
- ``classification_confusion_matrix.png`` / ``_NL.png`` — confusion matrix
"""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, GLOBAL_RANDOM_STATE, output_path


class Classification(PlotExample):

    # ``CCPlots / plot_configs / classification.json``
    CONFIG_KEY = "classification"

    # Change plot config to affect this.
    X, y = None, None
    class_cmap = None
    boundary_cmap = None
    confusion_cmap = None

    def __init__(self):
        super().__init__()
        self.classifier = LogisticRegression(max_iter=1000)

    def main(self):
        self.generate_data()

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.3, random_state=GLOBAL_RANDOM_STATE)

        self.class_cmap = mcolors.ListedColormap([
            self.resolve_color("class_0"),
            self.resolve_color("class_1"),
        ])
        self.boundary_cmap = mcolors.LinearSegmentedColormap.from_list(
            "bitroot_boundary",
            [BITROOT_PALETTE["surface"],
             self.resolve_color("boundary_region_0"),
             self.resolve_color("boundary_region_1")],
            N=256,
        )
        self.confusion_cmap = mcolors.LinearSegmentedColormap.from_list(
            "bitroot_confusion",
            [BITROOT_PALETTE["surface"],
             self.resolve_color("confusion_cmap_pale"),
             self.resolve_color("confusion_cmap")],
            N=256,
        )

        self.train_classifier()

        for _locale, labels, suffix in self.iter_locales():
            self.plot_decision_boundary(
                title=labels["decision_title"],
                xlabel=labels["xlabel"],
                ylabel=labels["ylabel"],
                legend_labels=(labels["legend_no_diabetes"], labels["legend_diabetes_positive"]),
                suffix=suffix,
            )

            self.plot_confusion_matrix(
                title=labels["confusion_title"],
                xlabel=labels["confusion_xlabel"],
                ylabel=labels["confusion_ylabel"],
                legend_labels=(labels["legend_no_diabetes"], labels["legend_diabetes_positive"]),
                cell_labels=labels,
                suffix=suffix,
            )

    def plot_confusion_matrix(self, title: str,
                              xlabel: str = "Predicted label",
                              ylabel: str = "True label",
                              legend_labels: tuple[str, str] | None = None,
                              cell_labels: dict | None = None,
                              suffix: str = "") -> None:
        y_pred = self.classifier.predict(self.X_test)
        cm = confusion_matrix(self.y_test, y_pred)

        cfigsize = self.config.panel_figsize("confusion_matrix")
        fig = plt.figure(figsize=cfigsize, facecolor=BITROOT_PALETTE['surface'])
        ax = plt.gca()
        ax.set_facecolor(BITROOT_PALETTE['white'])
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=self.classifier.classes_)
        disp.plot(cmap=self.confusion_cmap, values_format="d", ax=ax)
        self.apply_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel)

        if cell_labels is not None:
            labels_2x2 = [
                cell_labels.get("tn", "TN"),  cell_labels.get("tn_desc", ""),
                cell_labels.get("fp", "FP"),  cell_labels.get("fp_desc", ""),
                cell_labels.get("fn", "FN"),  cell_labels.get("fn_desc", ""),
                cell_labels.get("tp", "TP"),  cell_labels.get("tp_desc", ""),
            ]
            positions = [(0, 0), (1, 0), (0, 1), (1, 1)]
            for idx, (col, row) in enumerate(positions):
                text_color = disp.text_[row, col].get_color()
                abbrev = labels_2x2[idx * 2]
                desc = labels_2x2[idx * 2 + 1]
                ax.text(col, row + 0.28, abbrev, ha='center', va='center',
                        fontsize=9, fontweight='bold', color=text_color)
                ax.text(col, row - 0.28, desc, ha='center', va='center',
                        fontsize=7, color=text_color)

        self.apply_style(ax, background=BITROOT_PALETTE['white'])
        ax.grid(False)
        plt.tight_layout()
        fname = self.config.resolve_output("confusion_matrix", suffix=suffix)
        plt.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)

    def plot_decision_boundary(self, title: str,
                                xlabel: str = "Age",
                                ylabel: str = "Blood Pressure",
                                legend_labels: tuple[str, str] | None = None,
                                suffix: str = "") -> None:
        x_min, x_max = self.X[:, 0].min() - 1, self.X[:, 0].max() + 1
        y_min, y_max = self.X[:, 1].min() - 1, self.X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                             np.arange(y_min, y_max, 0.1))

        Z = self.classifier.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        fig, ax = self.create_figure()

        class_colors = [self.resolve_color('class_0'), self.resolve_color('class_1')]
        boundary_colors = [self.resolve_color('boundary_region_0'), self.resolve_color('boundary_region_1')]
        scatter_edge = self.resolve_color('scatter_edge')
        contour_color = self.resolve_color('contour_line')
        text_color = self.text_color

        for class_value in sorted(np.unique(self.y)):
            class_mask = self.y == class_value
            ax.scatter(self.X[class_mask, 0], self.X[class_mask, 1],
                       color=class_colors[class_value],
                       edgecolor=scatter_edge,
                       linewidth=0.6,
                       s=90,
                       label=f"Class {class_value}")

        decision_surface = ax.contourf(xx, yy, Z, levels=[-0.5, 0.5, 1.5], colors=boundary_colors, alpha=0.35)
        ax.contour(xx, yy, Z, colors=contour_color, linewidths=1.2, levels=[0.5])

        legend_text = legend_labels or ("No diabetes", "Diabetes positive")
        legend_handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=class_colors[0],
                       markeredgecolor=scatter_edge, markersize=8, label=legend_text[0]),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=class_colors[1],
                       markeredgecolor=scatter_edge, markersize=8, label=legend_text[1]),
        ]
        ax.legend(handles=legend_handles, frameon=False, loc='upper right', fontsize=10)

        self.apply_labels(ax, title=title, xlabel=xlabel, ylabel=ylabel)
        self.apply_style(ax)

        self.save_figure(fig, "decision_boundary", suffix=suffix)

    def generate_data(self) -> None:
        self.X, self.y = make_classification(
            n_samples=200,
            n_features=2,
            n_informative=2,
            n_redundant=0,
            n_clusters_per_class=1,
            n_classes=2,
            random_state=GLOBAL_RANDOM_STATE
        )

    def train_classifier(self) -> None:
        self.classifier.fit(self.X_train, self.y_train)


if __name__ == "__main__":
    Classification().main()

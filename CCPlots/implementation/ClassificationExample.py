"""
ClassificationExample.py

Plot an example of a classification problem. Generates a plot for the slides including a decision boundary
and a confusion matrix to help illustrate the concept.
"""

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path

RANDOM_SEED = 42

TEXT_BY_LOCALE = {
    "en": {
        "decision_title": "Classification Example with Decision Boundary",
        "confusion_title": "Confusion Matrix",
        "xlabel": "Age",
        "ylabel": "Blood Pressure",
        "confusion_xlabel": "Predicted label",
        "confusion_ylabel": "True label",
        "legend_no_diabetes": "No diabetes",
        "legend_diabetes_positive": "Diabetes positive",
    },
    "nl": {
        "decision_title": "Diabetes classificatievoorbeeld",
        "confusion_title": "Verwarringsmatrix",
        "xlabel": "Leeftijd",
        "ylabel": "Bloeddruk",
        "confusion_xlabel": "Voorspeld label",
        "confusion_ylabel": "Werkelijk label",
        "legend_no_diabetes": "Geen diabetes",
        "legend_diabetes_positive": "Diabetes positief",
    },
}


class ClassificationExample(PlotExample):

    # We will hold our data and classifier later
    X, y = None, None
    class_cmap = mcolors.ListedColormap([
        BITROOT_PALETTE["primary_soft"],
        BITROOT_PALETTE["secondary_light"],
    ])
    boundary_cmap = mcolors.LinearSegmentedColormap.from_list(
        "bitroot_boundary",
        [BITROOT_PALETTE["background"], BITROOT_PALETTE["primary_soft"], BITROOT_PALETTE["primary"]],
        N=256,
    )
    confusion_cmap = mcolors.LinearSegmentedColormap.from_list(
        "bitroot_confusion",
        [BITROOT_PALETTE["background"], BITROOT_PALETTE["primary_soft"], BITROOT_PALETTE["primary"]],
        N=256,
    )
    X_train, X_test, y_train, y_test = None, None, None, None
    classifier: LogisticRegression = None

    def main(self):
        """
        Execute a LR on synth data and plot a decision boundary and confusion matrix
        in English and Dutch
        """
        # Generate dummy data
        self.generate_data()

        # Split the data into training and testing sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            self.X, self.y, test_size=0.3, random_state=RANDOM_SEED)

        # Train LR classification model
        self.train_classifier()

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            self.plot_decision_boundary(
                fname=f"classification_decision_boundary{'_NL' if locale == 'nl' else ''}.png",
                title=labels["decision_title"],
                xlabel=labels["xlabel"],
                ylabel=labels["ylabel"],
                legend_labels=(labels["legend_no_diabetes"], labels["legend_diabetes_positive"]),
            )

            self.plot_confusion_matrix(
                fname=f"classification_confusion_matrix{'_NL' if locale == 'nl' else ''}.png",
                title=labels["confusion_title"],
                xlabel=labels["confusion_xlabel"],
                ylabel=labels["confusion_ylabel"],
                legend_labels=(labels["legend_no_diabetes"], labels["legend_diabetes_positive"]),
            )

    def plot_confusion_matrix(self, fname: str, title: str,
                              xlabel: str = "Predicted label",
                              ylabel: str = "True label",
                              legend_labels: tuple[str, str] | None = None) -> None:
        # Generate predictions and create a confusion matrix
        y_pred = self.classifier.predict(self.X_test)
        cm = confusion_matrix(self.y_test, y_pred)

        # Plot the confusion matrix
        fig = plt.figure(figsize=(6, 5), facecolor=BITROOT_PALETTE['background'])
        ax = plt.gca()
        ax.set_facecolor(BITROOT_PALETTE['card_background'])
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=self.classifier.classes_)
        disp.plot(cmap=self.confusion_cmap, values_format="d")
        plt.title(title, fontsize=16, color=BITROOT_PALETTE['text'], pad=10)
        plt.xlabel(xlabel, fontsize=14, color=BITROOT_PALETTE['text'])
        plt.ylabel(ylabel, fontsize=14, color=BITROOT_PALETTE['text'])
        apply_bitroot_style(ax, background=BITROOT_PALETTE['card_background'])
        plt.tight_layout()
        plt.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)

    def plot_decision_boundary(self, fname: str, title: str,
                               xlabel: str = "Age",
                               ylabel: str = "Blood Pressure",
                               legend_labels: tuple[str, str] | None = None) -> None:
        """ Plot the decision boundary and save the file with the desired text. """
        # Create a mesh to plot the decision boundary
        x_min, x_max = self.X[:, 0].min() - 1, self.X[:, 0].max() + 1
        y_min, y_max = self.X[:, 1].min() - 1, self.X[:, 1].max() + 1
        xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.1),
                             np.arange(y_min, y_max, 0.1))

        Z = self.classifier.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        # Plot the decision boundary
        plt.figure(figsize=(8, 6), facecolor=BITROOT_PALETTE['background'])
        ax = plt.gca()
        ax.set_facecolor(BITROOT_PALETTE['background'])

        class_colors = [BITROOT_PALETTE['primary'], BITROOT_PALETTE['secondary']]
        boundary_colors = [BITROOT_PALETTE['primary_soft'], BITROOT_PALETTE['secondary_soft']]
        for class_value in sorted(np.unique(self.y)):
            class_mask = self.y == class_value
            ax.scatter(self.X[class_mask, 0], self.X[class_mask, 1],
                       color=class_colors[class_value],
                       edgecolor=BITROOT_PALETTE['secondary_text'],
                       linewidth=0.6,
                       s=90,
                       label=f"Class {class_value}")

        decision_surface = ax.contourf(xx, yy, Z, levels=[-0.5, 0.5, 1.5], colors=boundary_colors, alpha=0.35)
        ax.contour(xx, yy, Z, colors=BITROOT_PALETTE['text'], linewidths=1.2, levels=[0.5])

        legend_text = legend_labels or ("No diabetes", "Diabetes positive")
        legend_handles = [
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=class_colors[0], markeredgecolor=BITROOT_PALETTE['secondary_text'], markersize=8, label=legend_text[0]),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=class_colors[1], markeredgecolor=BITROOT_PALETTE['secondary_text'], markersize=8, label=legend_text[1]),
        ]
        ax.legend(handles=legend_handles, frameon=False, loc='upper right', fontsize=10)

        plt.title(title, fontsize=16, color=BITROOT_PALETTE['text'], pad=10)
        plt.xlabel(xlabel, fontsize=14, color=BITROOT_PALETTE['text'])
        plt.ylabel(ylabel, fontsize=14, color=BITROOT_PALETTE['text'])
        apply_bitroot_style(ax)
        plt.tight_layout()
        plt.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)

    def generate_data(self) -> None:
        """ Generate some dummy data to simulate a diabetes classification problem. """
        # Generate a simple dataset for classification, where feature 1 is 'Age' and
        # feature 2 is 'Blood Pressure'
        self.X, self.y = make_classification(
            n_samples=200,
            n_features=2,
            n_informative=2,
            n_redundant=0,
            n_clusters_per_class=1,
            n_classes=2,
            random_state=RANDOM_SEED
        )

    def train_classifier(self) -> None:
        """ Train a Logistic Regression model on the data """
        # Train a simple logistic regression classifier
        self.classifier = LogisticRegression()
        self.classifier.fit(self.X_train, self.y_train)


if __name__ == "__main__":
    # Maintain this exactly, or we won't be able to regenerate every plot
    # resulting from this code.
    ClassificationExample().main()

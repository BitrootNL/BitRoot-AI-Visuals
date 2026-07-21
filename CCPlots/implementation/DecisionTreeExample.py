"""
DecisionTreeExample.py
"""
import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


class DecisionTreeExample(PlotExample):

    def main(self):
        # Load the iris dataset
        iris = load_iris()
        X, y = iris.data, iris.target

        # Train a decision tree classifier
        clf = DecisionTreeClassifier(max_depth=3)
        clf = clf.fit(X, y)

        # Plot the decision tree
        plt.figure(facecolor=BITROOT_PALETTE['background'])

        # This function does not accept many styling parameters at all, so we will have to suffer.
        tree.plot_tree(clf, filled=True, feature_names=iris.feature_names, class_names=iris.target_names)
        ax = plt.gca()
        apply_bitroot_style(ax)
        plt.tight_layout()
        plt.savefig(output_path("decision_tree_iris.png"))

import matplotlib.pyplot as plt
from sklearn import tree
from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Decision Tree on Iris Dataset",
    },
    "nl": {
        "title": "Beslissingsboom op Iris-dataset",
    },
}


class DecisionTreeExample(PlotExample):

    def main(self):
        iris = load_iris()
        X, y = iris.data, iris.target

        clf = DecisionTreeClassifier(max_depth=3)
        clf = clf.fit(X, y)

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"decision_tree_iris{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(10, 6), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            tree.plot_tree(clf, filled=True, feature_names=iris.feature_names,
                           class_names=iris.target_names, ax=ax)
            ax.set_title(labels["title"], color=BITROOT_PALETTE['text'])
            apply_bitroot_style(ax)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

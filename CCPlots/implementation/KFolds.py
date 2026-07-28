"""
Visualises 5-fold cross-validation splits as an imshow grid, highlighting
which samples belong to the training set (primary colour) and which to the
test set (tertiary colour) in each fold.

Figures
-------
- ``kfold_validation.png`` / ``_NL.png`` — fold-assignment grid

Configuration
-------------
``CCPlots/plot_configs/kfold.json``
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
from sklearn.datasets import make_classification
from sklearn.model_selection import KFold as SKFold

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, GLOBAL_RANDOM_STATE


class KFold(PlotExample):

    CONFIG_KEY = "kfold"

    colors = [BITROOT_PALETTE['primary'], BITROOT_PALETTE['tertiary']]

    def __init__(self):
        self.cmap = ListedColormap(self.colors)

    def main(self):
        X, _ = make_classification(n_samples=150, n_features=4, n_informative=3,
                                    n_redundant=0, random_state=GLOBAL_RANDOM_STATE)

        kf = SKFold(n_splits=5, shuffle=True, random_state=GLOBAL_RANDOM_STATE)
        n_samples = len(X)
        cv_splits = np.zeros((kf.get_n_splits(), n_samples))

        for i, (train_index, test_index) in enumerate(kf.split(X)):
            cv_splits[i, train_index] = 1
            cv_splits[i, test_index] = 2

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            im = ax.imshow(cv_splits, aspect='auto', cmap=self.cmap, interpolation='nearest')

            cbar = plt.colorbar(im, ax=ax, ticks=[1, 2])
            cbar.ax.set_yticklabels([labels['train'], labels['test']])
            cbar.set_label(labels['colorbar'], color=BITROOT_PALETTE['text'])
            cbar.ax.tick_params(colors=BITROOT_PALETTE['text'])

            ax.set_xlabel(labels['xlabel'], color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels['ylabel'], color=BITROOT_PALETTE['text'])
            ax.set_title(labels['title'], color=BITROOT_PALETTE['text'])

            self.apply_style(ax)
            self.save_figure(fig, "default", suffix=suffix)


if __name__ == "__main__":
    KFold().main()

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import KFold
from sklearn.datasets import make_classification

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Visualization of K-Fold Cross-Validation",
        "colorbar": "Fold number",
        "xlabel": "Index in the dataset",
        "ylabel": "Fold number",
        "train": "Training",
        "test": "Test",
    },
    "nl": {
        "title": "Visualisatie van K-Fold-kruisvalidatie",
        "colorbar": "Foldnummer",
        "xlabel": "Index in de dataset",
        "ylabel": "Foldnummer",
        "train": "Training",
        "test": "Test",
    },
}


class KFoldExample(PlotExample):

    colors = [BITROOT_PALETTE['primary'], BITROOT_PALETTE['tertiary']]

    def __init__(self):
        self.cmap = ListedColormap(self.colors)

    def main(self):
        X, _ = make_classification(n_samples=150, n_features=4, n_informative=3,
                                   n_redundant=0, random_state=42)

        kf = KFold(n_splits=5, shuffle=True, random_state=42)
        n_samples = len(X)
        cv_splits = np.zeros((kf.get_n_splits(), n_samples))

        for i, (train_index, test_index) in enumerate(kf.split(X)):
            cv_splits[i, train_index] = 1
            cv_splits[i, test_index] = 2

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"kfold_validation{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(10, 4), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            im = ax.imshow(cv_splits, aspect='auto', cmap=self.cmap, interpolation='nearest')

            cbar = plt.colorbar(im, ax=ax, ticks=[1, 2])
            cbar.ax.set_yticklabels([labels['train'], labels['test']])
            cbar.set_label(labels['colorbar'], color=BITROOT_PALETTE['text'])
            cbar.ax.tick_params(colors=BITROOT_PALETTE['text'])

            ax.set_xlabel(labels['xlabel'], color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels['ylabel'], color=BITROOT_PALETTE['text'])
            ax.set_title(labels['title'], color=BITROOT_PALETTE['text'])

            apply_bitroot_style(ax)
            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)


if __name__ == "__main__":
    KFoldExample().main()

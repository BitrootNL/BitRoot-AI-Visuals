import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap, to_rgba

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Logistic Regression Example: Spam vs. not spam",
        "xlabel": "Number of links in Email",
        "ylabel": "Email length (in characters)",
    },
    "nl": {
        "title": "Logistische regressie: spam versus geen spam",
        "xlabel": "Aantal links in e-mail",
        "ylabel": "E-maillengte (in karakters)",
    },
}


class LogisticRegressionExample(PlotExample):
    cmap_light = ListedColormap([
        to_rgba(BITROOT_PALETTE["background"], alpha=0.0),
        to_rgba(BITROOT_PALETTE["primary"], alpha=0.25),
    ])

    cmap_bold = [to_rgba(BITROOT_PALETTE["primary"], alpha=0.65), BITROOT_PALETTE["primary"]]

    accent = BITROOT_PALETTE['primary']

    def __init__(self, n_samples=200):
        self.n_samples = n_samples

        self.X, self.y = make_classification(
            n_samples=self.n_samples,
            n_features=2,
            n_informative=2,
            n_redundant=0,
            n_clusters_per_class=1,
            n_classes=2,
            random_state=42
        )

        self.model = LogisticRegression(solver='lbfgs')

    def update(self, frame):
        self.model.max_iter = frame + 1
        self.model.fit(self.X, self.y)

        Z = self.model.predict_proba(np.c_[self.xx.ravel(), self.yy.ravel()])[:, 1]
        Z = Z.reshape(self.xx.shape)

        for coll in self.ax.collections[:]:
            coll.remove()

        self.contourf = self.ax.contourf(self.xx, self.yy, Z, alpha=0.3, cmap=self.cmap_light)
        self.contour = self.ax.contour(self.xx, self.yy, Z, levels=[0.5], linewidths=2, colors=self.accent)

        return self.ax.collections + [self.scatter]

    def init_func(self):
        return self.ax.collections + [self.scatter]

    def main(self):
        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"logistic_regression_animation{'_NL' if locale == 'nl' else ''}.gif"

            fig, self.ax = plt.subplots()
            self.ax.set_xlim(self.X[:, 0].min() - 1, self.X[:, 0].max() + 1)
            self.ax.set_ylim(self.X[:, 1].min() - 1, self.X[:, 1].max() + 1)
            self.ax.set_title(labels["title"], fontsize=16, color=BITROOT_PALETTE['text'])
            self.ax.set_xlabel(labels["xlabel"], fontsize=14, color=BITROOT_PALETTE['text'])
            self.ax.set_ylabel(labels["ylabel"], fontsize=14, color=BITROOT_PALETTE['text'])

            self.xx, self.yy = np.meshgrid(
                np.arange(self.X[:, 0].min() - 1, self.X[:, 0].max() + 1, 0.1),
                np.arange(self.X[:, 1].min() - 1, self.X[:, 1].max() + 1, 0.1))

            Z = np.zeros_like(self.xx)
            self.contourf = self.ax.contourf(self.xx, self.yy, Z, alpha=0.8, cmap=self.cmap_light)
            self.contour = self.ax.contour(self.xx, self.yy, Z, levels=[0.5], linewidths=2, colors=self.accent)

            self.scatter = self.ax.scatter(self.X[:, 0], self.X[:, 1], c=self.y,
                                           cmap=ListedColormap(self.cmap_bold),
                                           edgecolor=self.accent, s=40)

            apply_bitroot_style(self.ax)

            ani = FuncAnimation(fig, self.update, frames=30, init_func=self.init_func, interval=200, repeat=False)

            ani.save(output_path(fname), writer='pillow')
            plt.close(fig)

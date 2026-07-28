"""
Animated logistic regression decision boundary for a spam-vs-not-spam
classification problem. The contour evolves over 30 solver iterations.

Figures
-------
- ``logistic_regression_animation.gif`` / ``_NL.gif`` — decision-boundary animation

Configuration
-------------
``CCPlots/plot_configs/logistic_regression.json``
"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="sklearn")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap, to_rgba
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression as SKLogisticRegression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, GLOBAL_RANDOM_STATE, output_path


class LogisticRegression(PlotExample):

    CONFIG_KEY = "logistic_regression"

    def __init__(self, n_samples=200):
        self.n_samples = n_samples

        self.X, self.y = make_classification(
            n_samples=self.n_samples,
            n_features=2,
            n_informative=2,
            n_redundant=0,
            n_clusters_per_class=1,
            n_classes=2,
            random_state=GLOBAL_RANDOM_STATE
        )

        self.model = SKLogisticRegression(solver='lbfgs', max_iter=1000)

    @property
    def cmap_light(self):
        return ListedColormap([
            to_rgba(BITROOT_PALETTE["background"], alpha=0.0),
            to_rgba(self.resolve_color('decision_boundary'), alpha=0.25),
        ])

    @property
    def cmap_bold(self):
        return [
            to_rgba(self.resolve_color('decision_boundary'), alpha=0.65),
            self.resolve_color('decision_boundary'),
        ]

    def update(self, frame):
        self.model.max_iter = frame + 1
        self.model.fit(self.X, self.y)

        Z = self.model.predict_proba(np.c_[self.xx.ravel(), self.yy.ravel()])[:, 1]
        Z = Z.reshape(self.xx.shape)

        # Remove only the contour collections, not the scatter
        for coll in [self.contourf, self.contour]:
            try:
                coll.remove()
            except (ValueError, KeyError):
                pass

        self.contourf = self.ax.contourf(self.xx, self.yy, Z, alpha=0.3, cmap=self.cmap_light)
        self.contour = self.ax.contour(self.xx, self.yy, Z, levels=[0.5], linewidths=2, colors=self.resolve_color('decision_boundary'))

        return self.ax.collections + [self.scatter]

    def init_func(self):
        return self.ax.collections + [self.scatter]

    def main(self):
        for _locale, labels, suffix in self.iter_locales():
            fig, self.ax = self.create_figure()
            self.ax.set_xlim(self.X[:, 0].min() - 1, self.X[:, 0].max() + 1)
            self.ax.set_ylim(self.X[:, 1].min() - 1, self.X[:, 1].max() + 1)
            self.ax.set_title(labels["title"], fontsize=16, color=self.text_color)
            self.ax.set_xlabel(labels["xlabel"], fontsize=14, color=self.text_color)
            self.ax.set_ylabel(labels["ylabel"], fontsize=14, color=self.text_color)

            self.xx, self.yy = np.meshgrid(
                np.arange(self.X[:, 0].min() - 1, self.X[:, 0].max() + 1, 0.1),
                np.arange(self.X[:, 1].min() - 1, self.X[:, 1].max() + 1, 0.1))

            Z = np.zeros_like(self.xx)
            self.contourf = self.ax.contourf(self.xx, self.yy, Z, alpha=0.8, cmap=self.cmap_light)
            self.contour = self.ax.contour(self.xx, self.yy, Z, levels=[0.5], linewidths=2, colors=self.resolve_color('decision_boundary'))

            self.scatter = self.ax.scatter(self.X[:, 0], self.X[:, 1], c=self.y,
                                           cmap=ListedColormap(self.cmap_bold),
                                           edgecolor=self.resolve_color('decision_boundary'), s=40)

            self.apply_style(self.ax)

            ani = FuncAnimation(fig, self.update, frames=30, init_func=self.init_func, interval=200, repeat=False)

            fname = self.config.resolve_output("animation", suffix=suffix)
            ani.save(output_path(fname), writer='pillow')
            plt.close(fig)

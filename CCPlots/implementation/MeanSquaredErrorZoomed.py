"""
Scatter plot with a single-iteration linear fit and vertical dashed
residuals, highlighting the difference between predicted and actual values
(used alongside the main MSE example for a zoomed-in view).

Figures
-------
- ``mse_zoom_iteration.png`` / ``_NL.png`` — residuals scatter

Configuration
-------------
``CCPlots/plot_configs/mse_zoom.json``
"""
from sklearn.datasets import make_regression
from sklearn.linear_model import SGDRegressor

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, GLOBAL_RANDOM_STATE


class MSEZoom(PlotExample):

    CONFIG_KEY = "mse_zoom"

    primary = BITROOT_PALETTE['primary']
    secondary = BITROOT_PALETTE['secondary']
    tertiary = BITROOT_PALETTE['tertiary']
    light_gray = BITROOT_PALETTE['grid']

    y_pred = None

    def __init__(self, n_samples=100, learning_rate=0.01):
        self.n_samples = n_samples
        self.learning_rate = learning_rate

        self.X, self.y = make_regression(
            n_samples=self.n_samples,
            n_features=1,
            noise=15,
            random_state=GLOBAL_RANDOM_STATE)

        self.model = SGDRegressor(
            max_iter=1,
            tol=None,
            learning_rate='constant',
            eta0=self.learning_rate,
            random_state=GLOBAL_RANDOM_STATE
        )

    def main(self):
        self.model.partial_fit(self.X, self.y)
        self.y_pred = self.model.predict(self.X)

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            ax.scatter(self.X, self.y, color=self.tertiary, label=labels['data_label'],
                       edgecolor=self.primary, linewidth=0.8, s=55, zorder=3)
            ax.plot(self.X, self.y_pred, color=self.primary, label=labels['line_label'],
                    linewidth=2.5, zorder=2)

            for i in range(len(self.X)):
                ax.plot([self.X[i], self.X[i]], [self.y[i], self.y_pred[i]],
                        color=self.primary, linestyle='--', alpha=0.35, linewidth=1.0, zorder=1)

            ax.set_title(labels['title'], fontsize=16, color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels['xlabel'], fontsize=14, color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels['ylabel'], fontsize=14, color=BITROOT_PALETTE['text'])

            self.apply_style(ax)
            ax.grid(True, color=self.light_gray)
            ax.legend()

            self.save_figure(fig, "default", suffix=suffix)

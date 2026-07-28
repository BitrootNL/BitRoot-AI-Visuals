"""
Scatter plot with a single-iteration linear fit and vertical dashed
residuals, highlighting the difference between predicted and actual values
(used alongside the main MSE example for a zoomed-in view).

Figures
-------
- ``mse_zoom_iteration.png`` / ``_NL.png`` — residuals scatter

Configuration
-------------
``CCPlots/plot_configs/mean_squared_error_zoomed.json``
"""
from sklearn.datasets import make_regression
from sklearn.linear_model import SGDRegressor

from CCPlots.PlotExample import PlotExample
from CCPlots.config import GLOBAL_RANDOM_STATE


class MeanSquaredErrorZoomed(PlotExample):

    CONFIG_KEY = "mean_squared_error_zoomed"

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

            ax.scatter(self.X, self.y, color=self.resolve_color('data_scatter'), label=labels['data_label'],
                       edgecolor=self.resolve_color('fitted_line'), linewidth=0.8, s=55, zorder=3)
            ax.plot(self.X, self.y_pred, color=self.resolve_color('fitted_line'), label=labels['line_label'],
                    linewidth=2.5, zorder=2)

            for i in range(len(self.X)):
                ax.plot([self.X[i], self.X[i]], [self.y[i], self.y_pred[i]],
                        color=self.resolve_color('residual_line'), linestyle='--', alpha=0.35, linewidth=1.0, zorder=1)

            self.apply_labels(ax, title=labels['title'], xlabel=labels['xlabel'],
                              ylabel=labels['ylabel'])

            self.apply_style(ax)
            ax.legend()

            self.save_figure(fig, "default", suffix=suffix)

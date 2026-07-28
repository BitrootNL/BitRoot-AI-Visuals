"""
Animated linear regression fitting a line to house-size vs. price data.
Data points are added one at a time, and the regression line updates
dynamically.

Figures
-------
- ``linear_regression_animation.gif`` / ``_NL.gif`` — animation

Configuration
-------------
``CCPlots/plot_configs/linear_regression.json``
"""
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.linear_model import LinearRegression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import GLOBAL_RANDOM_STATE, output_path


class LinearRegression(PlotExample):

    CONFIG_KEY = "linear_regression"

    def main(self):
        np.random.seed(GLOBAL_RANDOM_STATE)
        house_sizes = np.random.rand(100) * 2000 + 500
        prices = house_sizes * 200 + (np.random.randn(100) * 10000)

        sorted_indices = np.argsort(house_sizes)
        house_sizes = house_sizes[sorted_indices]
        prices = prices[sorted_indices]

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()
            ax.set_xlim(min(house_sizes) - 100, max(house_sizes) + 100)
            ax.set_ylim(min(prices) - 10000, max(prices) + 10000)
            ax.set_title(labels["title"], fontsize=16, color=self.text_color)
            ax.set_xlabel(labels["xlabel"], fontsize=14, color=self.text_color)
            ax.set_ylabel(labels["ylabel"], fontsize=14, color=self.text_color)

            scatter = ax.scatter(house_sizes, prices, color=self.resolve_color('data_points'),
                                 edgecolor=self.resolve_color('data_edge'), s=40)

            line, = ax.plot([], [], color=self.resolve_color('regression_line'), linewidth=2)

            def init():
                line.set_data([], [])
                return line,

            def update(frame):
                if frame < 2:
                    return line,

                X = house_sizes[:frame].reshape(-1, 1)
                y = prices[:frame]

                regressor = LinearRegression()
                regressor.fit(X, y)

                X_full = np.linspace(min(house_sizes), max(house_sizes), 100).reshape(-1, 1)
                y_pred = regressor.predict(X_full)

                line.set_data(X_full.flatten(), y_pred)

                return line,

            ani = FuncAnimation(fig, update, frames=len(house_sizes), init_func=init, blit=True, interval=10)

            self.apply_style(ax)

            fname = self.config.resolve_output("animation", suffix=suffix)
            ani.save(output_path(fname), writer='pillow')
            plt.close(fig)

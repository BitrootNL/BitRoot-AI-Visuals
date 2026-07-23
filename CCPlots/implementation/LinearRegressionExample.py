import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.linear_model import LinearRegression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Linear Regression Example: House Size vs. Price",
        "xlabel": "House Size (sq ft)",
        "ylabel": "Price ($)",
    },
    "nl": {
        "title": "Lineair regressievoorbeeld: huismaat vs. prijs",
        "xlabel": "Huismaat (m\u00b2)",
        "ylabel": "Prijs (\u20ac)",
    },
}


class LinearRegressionExample(PlotExample):

    primary = BITROOT_PALETTE['primary']

    def main(self):
        np.random.seed(42)
        house_sizes = np.random.rand(100) * 2000 + 500
        prices = house_sizes * 200 + (np.random.randn(100) * 10000)

        sorted_indices = np.argsort(house_sizes)
        house_sizes = house_sizes[sorted_indices]
        prices = prices[sorted_indices]

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"linear_regression_animation{'_NL' if locale == 'nl' else ''}.gif"

            fig, ax = plt.subplots(facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])
            ax.set_xlim(min(house_sizes) - 100, max(house_sizes) + 100)
            ax.set_ylim(min(prices) - 10000, max(prices) + 10000)
            ax.set_title(labels["title"], fontsize=16, color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels["xlabel"], fontsize=14, color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels["ylabel"], fontsize=14, color=BITROOT_PALETTE['text'])

            scatter = ax.scatter(house_sizes, prices, color=self.primary,
                                 edgecolor=BITROOT_PALETTE['secondary_text'], s=40)

            line, = ax.plot([], [], color=self.primary, linewidth=2)

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

            apply_bitroot_style(ax)

            ani.save(output_path(fname), writer='pillow')
            plt.close(fig)

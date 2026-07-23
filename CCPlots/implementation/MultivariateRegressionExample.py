import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.linear_model import LinearRegression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Multivariate Regression Example: House Size, Rooms vs. Price",
        "xlabel": "House Size (sq ft)",
        "ylabel": "Number of Rooms",
        "zlabel": "Price ($)",
    },
    "nl": {
        "title": "Multivariate regressie: huismaat, kamers vs. prijs",
        "xlabel": "Huismaat (m\u00b2)",
        "ylabel": "Aantal kamers",
        "zlabel": "Prijs (\u20ac)",
    },
}


class MultivariateRegressionExample(PlotExample):

    def main(self):
        np.random.seed(42)
        house_sizes = np.random.rand(100) * 2000 + 500
        num_rooms = np.random.rand(100) * 5 + 1
        prices = house_sizes * 150 + num_rooms * 20000 + (np.random.randn(100) * 10000)

        sorted_indices = np.argsort(house_sizes)
        house_sizes = house_sizes[sorted_indices]
        num_rooms = num_rooms[sorted_indices]
        prices = prices[sorted_indices]

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"multivariate_regression_animation{'_NL' if locale == 'nl' else ''}.gif"

            fig = plt.figure(figsize=(12, 8), facecolor=BITROOT_PALETTE['background'])
            ax = fig.add_subplot(111, projection='3d')
            fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)
            ax.set_facecolor(BITROOT_PALETTE['background'])
            ax.set_xlim(min(house_sizes) - 100, max(house_sizes) + 100)
            ax.set_ylim(min(num_rooms) - 1, max(num_rooms) + 1)
            ax.set_zlim(min(prices) - 10000, max(prices) + 10000)
            ax.set_title(labels["title"], fontsize=16, color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels["xlabel"], fontsize=14, color=BITROOT_PALETTE['text'], labelpad=18)
            ax.set_ylabel(labels["ylabel"], fontsize=14, color=BITROOT_PALETTE['text'], labelpad=18)
            ax.set_zlabel(labels["zlabel"], fontsize=14, color=BITROOT_PALETTE['text'], labelpad=18)
            ax.tick_params(pad=10)
            ax.dist = 12

            apply_bitroot_style(ax)

            scatter = ax.scatter(house_sizes, num_rooms, prices,
                                 color=BITROOT_PALETTE['primary'],
                                 edgecolor=BITROOT_PALETTE['primary'], s=45)

            house_sizes_grid, num_rooms_grid = np.meshgrid(
                np.linspace(min(house_sizes), max(house_sizes), 10),
                np.linspace(min(num_rooms), max(num_rooms), 10)
            )
            y_pred_initial = np.zeros_like(house_sizes_grid)

            plane = [ax.plot_surface(house_sizes_grid, num_rooms_grid, y_pred_initial,
                                     color=BITROOT_PALETTE['primary'], alpha=0.3)]

            def init():
                plane[0].remove()
                plane[0] = ax.plot_surface(house_sizes_grid, num_rooms_grid, y_pred_initial,
                                           color=BITROOT_PALETTE['primary'], alpha=0.3)
                return plane

            def update(frame):
                if frame < 3:
                    return plane

                X = np.column_stack((house_sizes[:frame], num_rooms[:frame]))
                y = prices[:frame]

                regressor = LinearRegression()
                regressor.fit(X, y)

                X_grid = np.column_stack((house_sizes_grid.ravel(), num_rooms_grid.ravel()))
                y_pred = regressor.predict(X_grid).reshape(house_sizes_grid.shape)

                plane[0].remove()
                plane[0] = ax.plot_surface(house_sizes_grid, num_rooms_grid, y_pred,
                                           color=BITROOT_PALETTE['primary'], alpha=0.3)

                return plane

            ani = FuncAnimation(fig, update, frames=len(house_sizes), init_func=init, blit=False, interval=100)

            ani.save(output_path(fname), writer='pillow')
            plt.close(fig)

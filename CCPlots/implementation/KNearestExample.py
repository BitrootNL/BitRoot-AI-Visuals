from typing import cast

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.axes3d import Axes3D
from sklearn.neighbors import KNeighborsRegressor

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "K-Nearest Neighbors for Housing",
        "xlabel": "House Size (sq ft)",
        "ylabel": "Number of Rooms",
        "zlabel": "Price ($)",
    },
    "nl": {
        "title": "K-dichtstbijzijnde buren voor huisvesting",
        "xlabel": "Huismaat (m\u00b2)",
        "ylabel": "Aantal kamers",
        "zlabel": "Prijs (\u20ac)",
    },
}


class KNearestExample(PlotExample):
    def main(self):
        np.random.seed(42)
        house_sizes = np.random.rand(100) * 2000 + 500
        num_rooms = np.random.rand(100) * 5 + 1
        prices = house_sizes * 150 + num_rooms * 20000 + (
                    np.random.randn(100) * 10000)

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"knn_visualization_animation{'_NL' if locale == 'nl' else ''}.gif"

            fig = plt.figure(figsize=(12, 8), facecolor=BITROOT_PALETTE['background'])
            ax = cast(Axes3D, fig.add_subplot(111, projection='3d'))
            fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)
            ax.set_facecolor(BITROOT_PALETTE['background'])
            ax.set_xlim(min(house_sizes) - 100, max(house_sizes) + 100)
            ax.set_ylim(min(num_rooms) - 1, max(num_rooms) + 1)
            ax.set_zlim(min(prices) - 10000, max(prices) + 10000)
            ax.set_title(labels["title"], color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels["xlabel"], color=BITROOT_PALETTE['text'], labelpad=18)
            ax.set_ylabel(labels["ylabel"], color=BITROOT_PALETTE['text'], labelpad=18)
            ax.set_zlabel(labels["zlabel"], color=BITROOT_PALETTE['text'], labelpad=18)
            ax.tick_params(pad=10)
            ax.dist = 12

            scatter = ax.scatter(house_sizes.tolist(), num_rooms.tolist(), prices.tolist(),
                                 color=BITROOT_PALETTE['primary'],
                                 edgecolor=BITROOT_PALETTE['primary'], s=60)

            knn = KNeighborsRegressor(n_neighbors=5)

            def init():
                return scatter,

            def update(frame):
                if frame < 5:
                    return scatter,

                X = np.column_stack((house_sizes[:frame], num_rooms[:frame]))
                y = prices[:frame]

                knn.fit(X, y)

                new_point = np.array([[house_sizes[frame], num_rooms[frame]]])
                predicted_price = knn.predict(new_point)

                ax.scatter(new_point[0, 0], new_point[0, 1], predicted_price[0],
                           color=BITROOT_PALETTE['primary'], label="New Point")
                ax.plot([new_point[0, 0], new_point[0, 0]], [new_point[0, 1], new_point[0, 1]],
                        [ax.get_zlim()[0], predicted_price[0]],
                        color=BITROOT_PALETTE['primary'], linestyle="--")

                return scatter,

            ani = FuncAnimation(fig, update, frames=len(house_sizes), init_func=init, blit=False, interval=200)

            apply_bitroot_style(ax)

            ani.save(output_path(fname), writer='pillow')
            plt.close(fig)

"""
3D animated K-Nearest Neighbors regression. Points are added sequentially
and the model predicts the price for each new point based on its closest
neighbours in house-size / room-count space.

Figures
-------
- ``knn_visualization_animation.gif`` / ``_NL.gif`` — 3D animation

Configuration
-------------
``CCPlots/plot_configs/knn.json``
"""
from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.axes3d import Axes3D
from sklearn.neighbors import KNeighborsRegressor

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, GLOBAL_RANDOM_STATE, output_path


class KNearest(PlotExample):

    CONFIG_KEY = "knn"

    def main(self):
        np.random.seed(GLOBAL_RANDOM_STATE)
        house_sizes = np.random.rand(100) * 2000 + 500
        num_rooms = np.random.rand(100) * 5 + 1
        prices = house_sizes * 150 + num_rooms * 20000 + (
                    np.random.randn(100) * 10000)

        for _locale, labels, suffix in self.iter_locales():
            fig = plt.figure(figsize=self.config.figsize, facecolor=BITROOT_PALETTE['background'])
            ax = cast(Axes3D, fig.add_subplot(111, projection='3d'))
            fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)
            ax.set_facecolor(BITROOT_PALETTE['background'])
            ax.set_xlim(min(house_sizes) - 100, max(house_sizes) + 100)
            ax.set_ylim(min(num_rooms) - 1, max(num_rooms) + 1)
            ax.set_zlim(min(prices) - 10000, max(prices) + 10000)
            ax.set_title(labels["title"], color=self.text_color)
            ax.set_xlabel(labels["xlabel"], color=self.text_color, labelpad=18)
            ax.set_ylabel(labels["ylabel"], color=self.text_color, labelpad=18)
            ax.set_zlabel(labels["zlabel"], color=self.text_color, labelpad=18)
            ax.tick_params(pad=10)
            ax.dist = 12

            scatter = ax.scatter(house_sizes.tolist(), num_rooms.tolist(), prices.tolist(),
                                 color=self.resolve_color('scatter'),
                                 edgecolor=self.resolve_color('scatter_edge'), s=60)

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
                           color=self.resolve_color('scatter'), label="New Point")
                ax.plot([new_point[0, 0], new_point[0, 0]], [new_point[0, 1], new_point[0, 1]],
                        [ax.get_zlim()[0], predicted_price[0]],
                        color=self.resolve_color('scatter'), linestyle="--")

                return scatter,

            ani = FuncAnimation(fig, update, frames=len(house_sizes), init_func=init, blit=False, interval=200)

            self.apply_style(ax)

            fname = self.config.resolve_output("animation", suffix=suffix)
            ani.save(output_path(fname), writer='pillow')
            plt.close(fig)

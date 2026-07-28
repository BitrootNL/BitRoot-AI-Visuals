"""
3D animated multivariate regression: a regression plane is fitted to
house-size / room-count vs. price data points as they are added one by one.

Figures
-------
- ``multivariate_regression_animation.gif`` / ``_NL.gif`` — 3D plane animation
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from sklearn.linear_model import LinearRegression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, GLOBAL_RANDOM_STATE, output_path


class MultivariateRegression(PlotExample):

    # CCPlots/plot_configs/multivariate_regression.json
    CONFIG_KEY = "multivariate_regression"

    def main(self):
        import warnings

        np.random.seed(GLOBAL_RANDOM_STATE)
        n_points = 100
        n_frames = 20
        house_sizes = np.random.rand(n_points) * 2000 + 500
        num_rooms = np.random.rand(n_points) * 5 + 1
        prices = house_sizes * 150 + num_rooms * 20000 + (np.random.randn(n_points) * 10000)

        sorted_indices = np.argsort(house_sizes)
        house_sizes = house_sizes[sorted_indices]
        num_rooms = num_rooms[sorted_indices]
        prices = prices[sorted_indices]

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            for _locale, labels, suffix in self.iter_locales():
                fig = plt.figure(figsize=self.config.figsize, facecolor=BITROOT_PALETTE['background'])
                ax = fig.add_subplot(111, projection='3d')
                fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)
                ax.set_facecolor(BITROOT_PALETTE['background'])
                ax.set_xlim(min(house_sizes) - 100, max(house_sizes) + 100)
                ax.set_ylim(min(num_rooms) - 1, max(num_rooms) + 1)
                ax.set_zlim(min(prices) - 10000, max(prices) + 10000)
                self.apply_labels(ax, title=labels["title"], xlabel=labels["xlabel"],
                                  ylabel=labels["ylabel"])
                ax.set_zlabel(labels["zlabel"], fontsize=14, color=self.text_color, labelpad=18)
                ax.tick_params(pad=10)
                ax.dist = 12

                self.apply_style(ax)

                scatter = ax.scatter(house_sizes, num_rooms, prices,
                                     color=self.resolve_color('scatter'),
                                     edgecolor=self.resolve_color('scatter_edge'), s=45)

                house_sizes_grid, num_rooms_grid = np.meshgrid(
                    np.linspace(min(house_sizes), max(house_sizes), 10),
                    np.linspace(min(num_rooms), max(num_rooms), 10)
                )
                y_pred_initial = np.zeros_like(house_sizes_grid)

                surf_color = self.resolve_color('surface')
                plane = [ax.plot_surface(house_sizes_grid, num_rooms_grid, y_pred_initial,
                                         color=surf_color, alpha=0.3)]

                def init():
                    plane[0].remove()
                    plane[0] = ax.plot_surface(house_sizes_grid, num_rooms_grid, y_pred_initial,
                                               color=surf_color, alpha=0.3)
                    return plane

                def update(frame):
                    step = n_points // n_frames
                    n_used = min((frame + 1) * step, n_points)

                    X = np.column_stack((house_sizes[:n_used], num_rooms[:n_used]))
                    y = prices[:n_used]

                    regressor = LinearRegression()
                    regressor.fit(X, y)

                    X_grid = np.column_stack((house_sizes_grid.ravel(), num_rooms_grid.ravel()))
                    y_pred = regressor.predict(X_grid).reshape(house_sizes_grid.shape)

                    plane[0].remove()
                    plane[0] = ax.plot_surface(house_sizes_grid, num_rooms_grid, y_pred,
                                               color=surf_color, alpha=0.3)

                    return plane

                ani = FuncAnimation(fig, update, frames=n_frames, init_func=init, blit=False, interval=100)

                fname = self.config.resolve_output("animation", suffix=suffix)
                ani.save(output_path(fname), writer='pillow')
                plt.close(fig)

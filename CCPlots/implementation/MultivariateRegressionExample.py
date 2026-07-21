"""
MultivariateRegressionExample.py

Create an animated plot of a multivariate linear regression example. The plot demonstrates the concept of multivariate
linear regression by visualizing how the regression plane evolves as more data points are added. This example uses
house prices based on the size of the house and the number of rooms.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.linear_model import LinearRegression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


class MultivariateRegressionExample(PlotExample):

    # Set colors for the plot
    primary = BITROOT_PALETTE['primary']
    light_gray = BITROOT_PALETTE['grid']

    def main(self):
        # Generate a simple dataset for multivariate linear regression (House Size, Number of Rooms vs. Price)
        np.random.seed(42)
        house_sizes = np.random.rand(100) * 2000 + 500  # House sizes between 500 and 2500 sq ft
        num_rooms = np.random.rand(100) * 5 + 1  # Number of rooms between 1 and 6
        prices = house_sizes * 150 + num_rooms * 20000 + (np.random.randn(100) * 10000)  # Price = 150 * size + 20000 * rooms + noise

        # Sort the data for better visualization
        sorted_indices = np.argsort(house_sizes)
        house_sizes = house_sizes[sorted_indices]
        num_rooms = num_rooms[sorted_indices]
        prices = prices[sorted_indices]

        # Create the figure and 3D axis for the animation
        fig = plt.figure(figsize=(14, 14), facecolor=BITROOT_PALETTE['background'])
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor(BITROOT_PALETTE['background'])
        ax.set_xlim(min(house_sizes) - 100, max(house_sizes) + 100)
        ax.set_ylim(min(num_rooms) - 1, max(num_rooms) + 1)
        ax.set_zlim(min(prices) - 10000, max(prices) + 10000)
        ax.set_title("Multivariate Regression Example: House Size, Rooms vs. Price", fontsize=16, color=BITROOT_PALETTE['text'])
        ax.set_xlabel("House Size (sq ft)", fontsize=14, color=BITROOT_PALETTE['text'])
        ax.set_ylabel("Number of Rooms", fontsize=14, color=BITROOT_PALETTE['text'])
        ax.set_zlabel("Price ($)", fontsize=14, color=BITROOT_PALETTE['text'])
        # Light gray grid
        plt.grid(True, color=self.light_gray)

        # Scatter plot of the data points
        scatter = ax.scatter(house_sizes, num_rooms, prices, color=self.primary, edgecolor=self.primary, s=45)

        # Create an initial meshgrid for the surface plot
        house_sizes_grid, num_rooms_grid = np.meshgrid(
            np.linspace(min(house_sizes), max(house_sizes), 10),
            np.linspace(min(num_rooms), max(num_rooms), 10)
        )
        y_pred_initial = np.zeros_like(house_sizes_grid)  # Initial Z values for the plane

        # Initialize the regression plane plot
        plane = [ax.plot_surface(house_sizes_grid, num_rooms_grid, y_pred_initial, color=self.primary, alpha=0.5)]

        # Function to initialize the animation
        def init():
            plane[0].remove()  # Remove the previous plot if exists
            plane[0] = ax.plot_surface(house_sizes_grid, num_rooms_grid, y_pred_initial, color=self.primary, alpha=0.5)
            return plane

        # Function to update the animation at each frame
        def update(frame):
            if frame < 3:  # Ensure at least 3 points are available for fitting
                return plane

            # Use data up to the current frame
            X = np.column_stack((house_sizes[:frame], num_rooms[:frame]))
            y = prices[:frame]

            # Perform multivariate linear regression
            regressor = LinearRegression()
            regressor.fit(X, y)

            # Predict values across the grid
            X_grid = np.column_stack((house_sizes_grid.ravel(), num_rooms_grid.ravel()))
            y_pred = regressor.predict(X_grid).reshape(house_sizes_grid.shape)

            # Remove the previous plot and add a new one
            plane[0].remove()
            plane[0] = ax.plot_surface(house_sizes_grid, num_rooms_grid, y_pred, color=self.primary, alpha=0.5)

            return plane

        # Create the animation
        ani = FuncAnimation(fig, update, frames=len(house_sizes), init_func=init, blit=False, interval=100)

        apply_bitroot_style(ax)

        # Save the animation as a GIF
        ani.save(output_path("multivariate_regression_animation.gif"), writer='pillow')

"""
KNNVisualizationExample.py

Create an animated plot of a K-Nearest Neighbors (KNN) classification example. The plot demonstrates the concept of KNN
by visualizing how a new data point is classified based on its nearest neighbors. This example uses house prices
based on the size of the house and the number of rooms.
"""

from typing import cast

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d.axes3d import Axes3D
from sklearn.neighbors import KNeighborsRegressor

from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


class KNearestExample:
    def main(self):
        # Generate a simple dataset (House Size, Number of Rooms vs. Price)
        np.random.seed(42)
        house_sizes = np.random.rand(100) * 2000 + 500  # House sizes between 500 and 2500 sq ft
        num_rooms = np.random.rand(100) * 5 + 1  # Number of rooms between 1 and 6
        prices = house_sizes * 150 + num_rooms * 20000 + (
                    np.random.randn(100) * 10000)  # Price = 150 * size + 20000 * rooms + noise

        # Create the figure and 3D axis for the animation
        fig = plt.figure(figsize=(12, 8), facecolor=BITROOT_PALETTE['background'])
        ax = cast(Axes3D, fig.add_subplot(111, projection='3d'))
        fig.subplots_adjust(left=0.05, right=0.95, top=0.92, bottom=0.05)
        ax.set_facecolor(BITROOT_PALETTE['background'])
        ax.set_xlim(min(house_sizes) - 100, max(house_sizes) + 100)
        ax.set_ylim(min(num_rooms) - 1, max(num_rooms) + 1)
        ax.set_zlim(min(prices) - 10000, max(prices) + 10000)
        ax.set_title("K-Nearest Neighbors for Housing", color=BITROOT_PALETTE['text'])
        ax.set_xlabel("House Size (sq ft)", color=BITROOT_PALETTE['text'], labelpad=18)
        ax.set_ylabel("Number of Rooms", color=BITROOT_PALETTE['text'], labelpad=18)
        ax.set_zlabel("Price ($)", color=BITROOT_PALETTE['text'], labelpad=18)
        ax.tick_params(pad=10)
        ax.dist = 12

        # Scatter plot of the data points using the Bitroot primary colour
        scatter = ax.scatter(house_sizes.tolist(), num_rooms.tolist(), prices.tolist(),
                             color=BITROOT_PALETTE['primary'],
                             edgecolor=BITROOT_PALETTE['primary'], s=60)

        # Initialize the KNN model
        knn = KNeighborsRegressor(n_neighbors=5)  # Using 5 nearest neighbors

        # Function to initialize the animation
        def init():
            return scatter,

        # Function to update the animation at each frame
        def update(frame):
            if frame < 5:  # Ensure at least 5 points are available for fitting
                return scatter,

            # Use data up to the current frame
            X = np.column_stack((house_sizes[:frame], num_rooms[:frame]))
            y = prices[:frame]

            # Fit the KNN model
            knn.fit(X, y)

            # New data point (for visualization purposes, we'll make it dynamic)
            new_point = np.array([[house_sizes[frame], num_rooms[frame]]])

            # Predict the price for the new data point
            predicted_price = knn.predict(new_point)

            # Plot the new point and the line connecting it to its predicted price
            ax.scatter(new_point[0, 0], new_point[0, 1], predicted_price[0],
                       color=BITROOT_PALETTE['primary'], label="New Point")
            ax.plot([new_point[0, 0], new_point[0, 0]], [new_point[0, 1], new_point[0, 1]],
                    [ax.get_zlim()[0], predicted_price[0]],
                    color=BITROOT_PALETTE['primary'], linestyle="--")

            return scatter,

        # Create the animation
        ani = FuncAnimation(fig, update, frames=len(house_sizes), init_func=init, blit=False, interval=200)

        apply_bitroot_style(ax)

        # Save the animation as a GIF
        ani.save(output_path("knn_visualization_animation.gif"), writer='pillow')

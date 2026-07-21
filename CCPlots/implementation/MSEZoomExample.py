"""
MSEZoomExample.py
"""

import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.datasets import make_regression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


class MSEZoomExample(PlotExample):

    # Set our colors from the palette
    primary = BITROOT_PALETTE['primary']
    secondary = BITROOT_PALETTE['secondary']
    tertiary = BITROOT_PALETTE['tertiary']
    light_gray = BITROOT_PALETTE['grid']

    # Array for the final predictions
    y_pred = None

    def __init__(self, n_samples=100, learning_rate=0.01):
        self.n_samples = n_samples
        self.learning_rate = learning_rate

        # Generate synthetic data for regression
        self.X, self.y = make_regression(
            n_samples=self.n_samples,
            n_features=1,
            noise=15,
            random_state=42)

        # Initialize the model
        self.model = SGDRegressor(
            max_iter=1,
            tol=None,
            learning_rate='constant',
            eta0=self.learning_rate,
            random_state=42
        )

    def main(self):
        """Main method to train and plot the MSE zoom."""
        self.train_one_iteration()
        self.plot_mse_zoom()

    def train_one_iteration(self):
        """Train the model for one iteration and get the predictions."""
        self.model.partial_fit(self.X, self.y)  # Perform one iteration of training
        self.y_pred = self.model.predict(self.X)

    def plot_mse_zoom(self):
        """Plot the data points, the fitted line, and the errors."""
        plt.figure(figsize=(10, 6), facecolor=BITROOT_PALETTE['background'])

        # Plot data points
        plt.scatter(self.X, self.y, color=self.secondary, label='Data points', edgecolor=self.primary)

        # Plot the fitted line
        plt.plot(self.X, self.y_pred, color=self.primary, label='Fitted line')

        # Plot the errors
        for i in range(len(self.X)):
            plt.plot([self.X[i], self.X[i]], [self.y[i], self.y_pred[i]], color=self.tertiary, linestyle='--', alpha=0.6)

        # Title and labels
        plt.title('Differences between predicted function and actual values', fontsize=16, color=BITROOT_PALETTE['text'])
        plt.xlabel("X value (feature)", fontsize=14, color=BITROOT_PALETTE['text'])
        plt.ylabel("Y value (prediction/actual)", fontsize=14, color=BITROOT_PALETTE['text'])

        ax = plt.gca()
        apply_bitroot_style(ax)
        ax.grid(True, color=self.light_gray)

        # Add legend
        plt.legend()

        # Save the plot to the specified output path
        plt.savefig(output_path("mse_zoom_iteration.png"))

if __name__ == "__main__":
    MSEZoomExample().main()

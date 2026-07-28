"""
Line chart of Mean Squared Error over 50 SGD iterations, illustrating the
convergence behaviour of a linear regression model trained via stochastic
gradient descent.

Figures
-------
- ``mse_over_iterations.png`` / ``_NL.png`` — MSE convergence line

Configuration
-------------
``CCPlots/plot_configs/mse.json``
"""
from sklearn.datasets import make_regression
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE


class MSE(PlotExample):
    CONFIG_KEY = "mse"

    primary = BITROOT_PALETTE['primary']
    light_gray = BITROOT_PALETTE['grid']

    def __init__(self, n_samples=100, iterations=50, learning_rate=0.01):
        self.n_samples = n_samples
        self.iterations = iterations
        self.learning_rate = learning_rate

        self.X, self.y = make_regression(n_samples=self.n_samples, n_features=1, noise=15, random_state=42)

        self.model = SGDRegressor(max_iter=1, tol=None, learning_rate='constant', eta0=self.learning_rate,
                                  random_state=42)

        self.mse_values = []

    def main(self):
        self.train_and_calculate_mse()

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            ax.plot(range(1, self.iterations + 1), self.mse_values, color=self.primary, marker='o')
            ax.set_title(labels['title'], fontsize=16, color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels['xlabel'], fontsize=14, color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels['ylabel'], fontsize=14, color=BITROOT_PALETTE['text'])

            self.apply_style(ax)
            ax.grid(True, color=self.light_gray)

            self.save_figure(fig, "default", suffix=suffix)

    def train_and_calculate_mse(self):
        for _ in range(self.iterations):
            self.model.partial_fit(self.X, self.y)
            y_pred = self.model.predict(self.X)
            mse = mean_squared_error(self.y, y_pred)
            self.mse_values.append(mse)

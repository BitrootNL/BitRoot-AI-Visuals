"""
2 x 3 subplot grid of six common neural-network activation functions:
Sigmoid, Tanh, ReLU, Leaky ReLU, Swish, and Softplus. Each curve is
drawn in a distinct Bitroot palette colour.

Figures
-------
- ``neural_network_activation_functions.png`` / ``_NL.png`` — 2x3 activation grid

Configuration
-------------
``CCPlots/plot_configs/neural_network_activation.json``
"""
import numpy as np

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE


class NeuralNetworkActivationFunctions(PlotExample):

    CONFIG_KEY = "neural_network_activation"

    def main(self):
        x = np.linspace(-10, 10, 400)

        func_specs = [
            (self.sigmoid, "sigmoid"),
            (self.tanh, "tanh"),
            (self.relu, "relu"),
            (self.leaky_relu, "leaky_relu"),
            (self.swish, "swish"),
            (self.softplus, "softplus"),
        ]

        for _locale, labels, suffix in self.iter_locales():
            fig, axs = self.create_figure(nrows=2, ncols=3)

            for idx, (func, color_key) in enumerate(func_specs):
                row, col = divmod(idx, 3)
                ax = axs[row, col]
                ax.plot(x, func(x), color=self.resolve_color(color_key), linewidth=2)
                ax.set_title(labels[color_key], color=self.text_color)
                self.apply_style(ax)
                ax.grid(True, color=self.resolve_color('grid'))

            fig.suptitle(labels["title"], fontsize=16, color=self.text_color, y=1.02)

            self.save_figure(fig, "default", suffix=suffix)

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def tanh(self, x):
        return np.tanh(x)

    def relu(self, x):
        return np.maximum(0, x)

    def leaky_relu(self, x, alpha=0.01):
        return np.where(x > 0, x, alpha * x)

    def swish(self, x):
        return x * self.sigmoid(x)

    def softplus(self, x):
        return np.log(1 + np.exp(x))

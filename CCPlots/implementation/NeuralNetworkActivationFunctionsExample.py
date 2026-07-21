"""
NeuralNetworkActivationFunctionsExample.py
"""
import numpy as np
import matplotlib.pyplot as plt

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


class NeuralNetworkActivationFunctionsExample(PlotExample):

    # Line colors
    primary = BITROOT_PALETTE["primary"]
    secondary = BITROOT_PALETTE["secondary"]
    tertiary = BITROOT_PALETTE["tertiary"]
    highlight = BITROOT_PALETTE["highlight"]
    success = BITROOT_PALETTE["success"]
    info = BITROOT_PALETTE["info"]

    # Grid
    light_gray = BITROOT_PALETTE['grid']

    def main(self):
        # Define the range of inputs
        x = np.linspace(-10, 10, 400)

        # Plotting the activation functions
        plt.figure(figsize=(12, 8), facecolor=BITROOT_PALETTE['background'])

        for idx, (func, color, title) in enumerate([
            (self.sigmoid, self.primary, 'Sigmoid'),
            (self.tanh, self.secondary, 'Tanh'),
            (self.relu, self.tertiary, 'ReLU'),
            (self.leaky_relu, self.info, 'Leaky ReLU'),
            (self.swish, self.success, 'Swish'),
            (self.softplus, self.highlight, 'Softplus'),
        ], start=1):
            plt.subplot(2, 3, idx)
            plt.plot(x, func(x), color=color, linewidth=2)
            plt.title(title, color=BITROOT_PALETTE['text'])
            ax = plt.gca()
            apply_bitroot_style(ax, background=BITROOT_PALETTE['background'])
            ax.grid(True, color=self.light_gray)

        plt.tight_layout()
        plt.savefig(output_path("neural_network_activation_functions.png"))

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

if __name__ == "__main__":
    NeuralNetworkActivationFunctionsExample().main()

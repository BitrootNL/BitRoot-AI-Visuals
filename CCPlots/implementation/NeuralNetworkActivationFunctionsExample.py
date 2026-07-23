import numpy as np
import matplotlib.pyplot as plt

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Neural Network Activation Functions",
        "sigmoid": "Sigmoid",
        "tanh": "Tanh",
        "relu": "ReLU",
        "leaky_relu": "Leaky ReLU",
        "swish": "Swish",
        "softplus": "Softplus",
    },
    "nl": {
        "title": "Neurale netwerk activatiefuncties",
        "sigmoid": "Sigmoid",
        "tanh": "Tanh",
        "relu": "ReLU",
        "leaky_relu": "Leaky ReLU",
        "swish": "Swish",
        "softplus": "Softplus",
    },
}


class NeuralNetworkActivationFunctionsExample(PlotExample):

    primary = BITROOT_PALETTE["primary"]
    secondary = BITROOT_PALETTE["secondary"]
    tertiary = BITROOT_PALETTE["tertiary"]
    highlight = BITROOT_PALETTE["highlight"]
    success = BITROOT_PALETTE["success"]
    info = BITROOT_PALETTE["info"]

    light_gray = BITROOT_PALETTE['grid']

    def main(self):
        x = np.linspace(-10, 10, 400)

        func_specs = [
            (self.sigmoid, self.primary, "sigmoid"),
            (self.tanh, self.secondary, "tanh"),
            (self.relu, self.tertiary, "relu"),
            (self.leaky_relu, self.info, "leaky_relu"),
            (self.swish, self.success, "swish"),
            (self.softplus, self.highlight, "softplus"),
        ]

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"neural_network_activation_functions{'_NL' if locale == 'nl' else ''}.png"

            fig, axs = plt.subplots(2, 3, figsize=(12, 8),
                                    facecolor=BITROOT_PALETTE['background'])
            fig.patch.set_facecolor(BITROOT_PALETTE['background'])

            for idx, (func, color, key) in enumerate(func_specs):
                row, col = divmod(idx, 3)
                ax = axs[row, col]
                ax.plot(x, func(x), color=color, linewidth=2)
                ax.set_title(labels[key], color=BITROOT_PALETTE['text'])
                apply_bitroot_style(ax, background=BITROOT_PALETTE['background'])
                ax.grid(True, color=self.light_gray)

            fig.suptitle(labels["title"], fontsize=16, color=BITROOT_PALETTE['text'], y=1.02)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

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

"""
Demonstrates the concept of noise in data by plotting a clean sin(x) curve
alongside noisy observations sampled from a Gaussian distribution around it.

Figures
-------
- ``noisy_data.png`` / ``_NL.png`` — clean curve + noisy scatter

Configuration
-------------
``CCPlots/plot_configs/noisy_data.json``
"""
import numpy as np

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE


class NoisyData(PlotExample):

    CONFIG_KEY = "noisy_data"

    primary: str = BITROOT_PALETTE['primary']
    tertiary: str = BITROOT_PALETTE['tertiary']

    def main(self) -> None:
        x = np.linspace(0, 10, 100)
        y_actual = np.sin(x)
        noise = np.random.normal(0, 0.3, size=x.shape)
        y_noisy = y_actual + noise

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            ax.plot(x, y_actual, label=labels["true_label"], color=self.primary, linewidth=2)
            ax.scatter(x, y_noisy, label=labels["noisy_label"], color=self.tertiary, alpha=0.6)

            ax.set_xlabel(labels["xlabel"], color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels["ylabel"], color=BITROOT_PALETTE['text'])
            ax.set_title(labels["title"], color=BITROOT_PALETTE['text'])
            ax.legend()

            self.apply_style(ax)
            self.save_figure(fig, "default", suffix=suffix)


if __name__ == "__main__":
    NoisyData().main()

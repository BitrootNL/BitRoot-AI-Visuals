"""
RegressionExample.py

Plot an example of a distribution we would use for a regression problem. Generates a plot for the slides.
"""

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

from CCPlots.PlotExample import PlotExample
from CCPlots.config import OUTPUT_PATH, BITROOT_PALETTE, apply_bitroot_style


class RegressionExample(PlotExample):

    # Configure the colours for the plot
    primary = BITROOT_PALETTE['primary']
    secondary = BITROOT_PALETTE['secondary']
    tertiary = BITROOT_PALETTE['tertiary']
    calm_blue = '#5C78D9'
    calm_purple = '#7AAED6'

    def main(self):

        # Generate data for the normal distribution curve
        mean = 159
        std_dev = 6.1
        x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
        y = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev)**2)

        # Plot the normal distribution
        plt.figure(figsize=(10, 6), facecolor=BITROOT_PALETTE['background'])
        plt.plot(x, y, label="Female Height Distribution World-wide", color=self.primary)

        # Shade the regions under the curve
        plt.fill_between(x, y, where=(x <= mean - 2*std_dev), color=self.tertiary, alpha=0.22)
        plt.fill_between(x, y, where=((x > mean - 2*std_dev) & (x <= mean - std_dev)), color=self.calm_blue, alpha=0.25)
        plt.fill_between(x, y, where=((x > mean - std_dev) & (x < mean + std_dev)), color=self.calm_purple, alpha=0.18)
        plt.fill_between(x, y, where=((x >= mean + std_dev) & (x < mean + 2*std_dev)), color=self.calm_blue, alpha=0.25)
        plt.fill_between(x, y, where=(x >= mean + 2*std_dev), color=self.tertiary, alpha=0.22)

        # Add labels for the IQ scores and standard deviations
        plt.axvline(mean, color=self.secondary, linestyle='dashed', linewidth=1)
        plt.axvline(mean - std_dev, color=self.secondary, linestyle='dashed', linewidth=1)
        plt.axvline(mean + std_dev, color=self.secondary, linestyle='dashed', linewidth=1)
        plt.axvline(mean - 2*std_dev, color=self.secondary, linestyle='dashed', linewidth=1)
        plt.axvline(mean + 2*std_dev, color=self.secondary, linestyle='dashed', linewidth=1)

        plt.text(mean, max(y)*0.9, '100', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)
        plt.text(mean - std_dev, max(y)*0.9, '85', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)
        plt.text(mean + std_dev, max(y)*0.9, '115', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)
        plt.text(mean - 2*std_dev, max(y)*0.9, '70', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)
        plt.text(mean + 2*std_dev, max(y)*0.9, '130', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)

        # Set plot labels and title
        plt.title("Female Height Distribution World-wide", fontsize=16, color=BITROOT_PALETTE['text'])
        plt.xlabel("Height in cms (mean=159, std=6.1)", fontsize=14, color=BITROOT_PALETTE['text'])
        plt.ylabel("Probability Density", fontsize=14, color=BITROOT_PALETTE['text'])
        plt.grid(True)

        # Customize the x-axis
        ax = plt.gca()
        ax = apply_bitroot_style(ax)
        ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
        ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color=BITROOT_PALETTE['grid'])
        ax.set_ylim(0, max(y) * 1.1)

        # Show the plot
        plt.savefig(OUTPUT_PATH + "regression_example.png")


if __name__ == "__main__":
    RegressionExample().main()

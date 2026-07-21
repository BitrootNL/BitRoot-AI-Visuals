"""
NeuralNetworkGrowthExample.py
"""

import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


class NeuralNetworkGrowthExample(PlotExample):

    # Plot colours
    primary = BITROOT_PALETTE['primary']
    tertiary = BITROOT_PALETTE['tertiary']
    light_gray = BITROOT_PALETTE['grid']

    def main(self):
        # Data for the models
        years = [2012, 2014, 2018, 2020]
        models = ["AlexNet", "VGG-16", "BERT", "GPT-3"]
        parameters = [60e6, 138e6, 340e6, 175e9]

        # Plotting the line figure
        plt.figure(figsize=(10, 6), facecolor=BITROOT_PALETTE['background'])
        plt.plot(years, parameters, marker='o', color=self.primary, linewidth=2.5, markersize=7)
        plt.fill_between(years, parameters, color=to_rgba(self.primary, alpha=0.18))
        for i, txt in enumerate(models):
            plt.text(years[i], parameters[i], txt, fontsize=10, ha='right', color=BITROOT_PALETTE['text'])

        # Plot y logarithmically (exponential growth)
        plt.yscale('log')

        # Plot labeling
        plt.title("Growth in Neural Network Parameters Over Time", fontsize=14, color=BITROOT_PALETTE['text'])
        plt.xlabel("Year", color=BITROOT_PALETTE['text'])
        plt.xlim(min(years), max(years))
        plt.ylabel("Parameters (log scale)", color=BITROOT_PALETTE['text'])

        ax = plt.gca()
        apply_bitroot_style(ax)
        ax.grid(True, color=self.light_gray)
        plt.savefig(output_path("neural_network_growth_line_log.png"))


if __name__ == "__main__":
    NeuralNetworkGrowthExample().main()

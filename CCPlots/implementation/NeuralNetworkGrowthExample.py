"""
Log-scale line chart tracking the explosion of learnable parameters in
landmark neural networks from AlexNet (2012, 60M) to GPT-3 (2020, 175B).

Figures
-------
- ``neural_network_growth_line_log.png`` / ``_NL.png`` — log-scale growth line

Configuration
-------------
``CCPlots/plot_configs/neural_network_growth.json``
"""
from matplotlib.colors import to_rgba

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE


class NeuralNetworkGrowth(PlotExample):

    CONFIG_KEY = "neural_network_growth"

    primary = BITROOT_PALETTE['primary']
    light_gray = BITROOT_PALETTE['grid']

    def main(self):
        years = [2012, 2014, 2018, 2020]
        models = ["AlexNet", "VGG-16", "BERT", "GPT-3"]
        parameters = [60e6, 138e6, 340e6, 175e9]

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            ax.plot(years, parameters, marker='o', color=self.primary, linewidth=2.5, markersize=7)
            ax.fill_between(years, parameters, color=to_rgba(self.primary, alpha=0.18))
            for i, txt in enumerate(models):
                ax.text(years[i], parameters[i], txt, fontsize=10, ha='right', color=BITROOT_PALETTE['text'])

            ax.set_yscale('log')

            ax.set_title(labels['title'], fontsize=14, color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels['xlabel'], color=BITROOT_PALETTE['text'])
            ax.set_xlim(min(years), max(years))
            ax.set_ylabel(labels['ylabel'], color=BITROOT_PALETTE['text'])

            self.apply_style(ax)
            ax.grid(True, color=self.light_gray)

            self.save_figure(fig, "default", suffix=suffix)

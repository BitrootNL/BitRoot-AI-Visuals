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

class NeuralNetworkGrowth(PlotExample):

    CONFIG_KEY = "neural_network_growth"

    def main(self):
        years = [2012, 2014, 2018, 2020]
        models = ["AlexNet", "VGG-16", "BERT", "GPT-3"]
        parameters = [60e6, 138e6, 340e6, 175e9]

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            ax.plot(years, parameters, marker='o', color=self.resolve_color('growth_line'), linewidth=2.5, markersize=7)
            ax.fill_between(years, parameters, color=to_rgba(self.resolve_color('growth_line'), alpha=0.18))
            for i, txt in enumerate(models):
                ax.text(years[i], parameters[i], txt, fontsize=10, ha='right', color=self.text_color)

            ax.set_yscale('log')

            self.apply_labels(ax, title=labels['title'], xlabel=labels['xlabel'],
                              ylabel=labels['ylabel'])

            self.apply_style(ax)

            self.save_figure(fig, "default", suffix=suffix)

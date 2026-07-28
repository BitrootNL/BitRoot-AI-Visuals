"""
Normal distribution curve of female height with shaded standard-deviation
regions (68 %, 95 %), dashed mean markers, and highlighted interval labels.

Figures
-------
- ``normal_distribution.png`` / ``_NL.png`` — bell curve with SD bands

Configuration
-------------
``CCPlots/plot_configs/normal_distribution.json``
"""
import matplotlib.ticker as ticker
import numpy as np

from CCPlots.PlotExample import PlotExample


class NormalDistribution(PlotExample):

    CONFIG_KEY = "normal_distribution"

    def main(self):
        mean = 159
        std_dev = 6.1
        x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
        y = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev)**2)

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            ax.plot(x, y, label=labels['label_line'], color=self.resolve_color('line'))

            ax.fill_between(x, y, where=(x <= mean - 2 * std_dev).tolist(),
                            color=self.resolve_color('outer_band'))
            ax.fill_between(x, y, where=((x > mean - 2 * std_dev) & (x <= mean - std_dev)).tolist(),
                            color=self.resolve_color('inner_band'))
            ax.fill_between(x, y, where=((x > mean - std_dev) & (x < mean + std_dev)).tolist(),
                            color=self.resolve_color('middle_band'))
            ax.fill_between(x, y, where=((x >= mean + std_dev) & (x < mean + 2 * std_dev)).tolist(),
                            color=self.resolve_color('inner_band'))
            ax.fill_between(x, y, where=(x >= mean + 2 * std_dev).tolist(),
                            color=self.resolve_color('outer_band'))

            div = self.resolve_color('divider')
            ax.axvline(mean, color=div, linestyle='dashed', linewidth=1)
            ax.axvline(mean - std_dev, color=div, linestyle='dashed', linewidth=1)
            ax.axvline(mean + std_dev, color=div, linestyle='dashed', linewidth=1)
            ax.axvline(mean - 2*std_dev, color=div, linestyle='dashed', linewidth=1)
            ax.axvline(mean + 2*std_dev, color=div, linestyle='dashed', linewidth=1)

            text_color = self.text_color
            ax.text(mean, max(y)*0.9, '100', ha='center', color=text_color, fontsize=12)
            ax.text(mean - std_dev, max(y)*0.9, '85', ha='center', color=text_color, fontsize=12)
            ax.text(mean + std_dev, max(y)*0.9, '115', ha='center', color=text_color, fontsize=12)
            ax.text(mean - 2*std_dev, max(y)*0.9, '70', ha='center', color=text_color, fontsize=12)
            ax.text(mean + 2*std_dev, max(y)*0.9, '130', ha='center', color=text_color, fontsize=12)

            self.apply_labels(ax, title=labels['title'], xlabel=labels['xlabel'],
                              ylabel=labels['ylabel'])

            self.apply_style(ax)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
            ax.grid(True, which='both', linestyle='--', linewidth=0.5)
            ax.set_ylim(0, max(y) * 1.1)

            self.save_figure(fig, "default", suffix=suffix)

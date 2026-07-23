import matplotlib.pyplot as plt
import numpy as np
import matplotlib.ticker as ticker

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Female Height Distribution World-wide",
        "xlabel": "Height in cms (mean=159, std=6.1)",
        "ylabel": "Probability Density",
        "label_line": "Female Height Distribution World-wide",
    },
    "nl": {
        "title": "Wereldwijde lengteverdeling van vrouwen",
        "xlabel": "Lengte in cm (gem=159, std=6.1)",
        "ylabel": "Kansdichtheid",
        "label_line": "Wereldwijde lengteverdeling van vrouwen",
    },
}


class RegressionExample(PlotExample):

    primary = BITROOT_PALETTE['primary']
    secondary = BITROOT_PALETTE['secondary']
    tertiary = BITROOT_PALETTE['tertiary']
    calm_blue = '#5C78D9'
    calm_purple = '#7AAED6'

    def main(self):
        mean = 159
        std_dev = 6.1
        x = np.linspace(mean - 4*std_dev, mean + 4*std_dev, 1000)
        y = (1/(std_dev * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mean) / std_dev)**2)

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"regression_example{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(10, 6), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            ax.plot(x, y, label=labels['label_line'], color=self.primary)

            ax.fill_between(x, y, where=(x <= mean - 2 * std_dev).tolist(), color=self.tertiary, alpha=0.22)
            ax.fill_between(x, y, where=((x > mean - 2 * std_dev) & (x <= mean - std_dev)).tolist(),
                            color=self.calm_blue, alpha=0.25)
            ax.fill_between(x, y, where=((x > mean - std_dev) & (x < mean + std_dev)).tolist(),
                            color=self.calm_purple, alpha=0.18)
            ax.fill_between(x, y, where=((x >= mean + std_dev) & (x < mean + 2 * std_dev)).tolist(),
                            color=self.calm_blue, alpha=0.25)
            ax.fill_between(x, y, where=(x >= mean + 2 * std_dev).tolist(), color=self.tertiary, alpha=0.22)

            ax.axvline(mean, color=self.secondary, linestyle='dashed', linewidth=1)
            ax.axvline(mean - std_dev, color=self.secondary, linestyle='dashed', linewidth=1)
            ax.axvline(mean + std_dev, color=self.secondary, linestyle='dashed', linewidth=1)
            ax.axvline(mean - 2*std_dev, color=self.secondary, linestyle='dashed', linewidth=1)
            ax.axvline(mean + 2*std_dev, color=self.secondary, linestyle='dashed', linewidth=1)

            ax.text(mean, max(y)*0.9, '100', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)
            ax.text(mean - std_dev, max(y)*0.9, '85', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)
            ax.text(mean + std_dev, max(y)*0.9, '115', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)
            ax.text(mean - 2*std_dev, max(y)*0.9, '70', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)
            ax.text(mean + 2*std_dev, max(y)*0.9, '130', ha='center', color=BITROOT_PALETTE['text'], fontsize=12)

            ax.set_title(labels['title'], fontsize=16, color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels['xlabel'], fontsize=14, color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels['ylabel'], fontsize=14, color=BITROOT_PALETTE['text'])

            apply_bitroot_style(ax)
            ax.xaxis.set_major_locator(ticker.MultipleLocator(15))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(5))
            ax.grid(True, which='both', linestyle='--', linewidth=0.5, color=BITROOT_PALETTE['grid'])
            ax.set_ylim(0, max(y) * 1.1)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

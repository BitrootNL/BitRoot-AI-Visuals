import matplotlib.pyplot as plt
from matplotlib.colors import to_rgba

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Growth in Neural Network Parameters Over Time",
        "xlabel": "Year",
        "ylabel": "Parameters (log scale)",
    },
    "nl": {
        "title": "Groei van neurale netwerkparameters door de tijd",
        "xlabel": "Jaar",
        "ylabel": "Parameters (log schaal)",
    },
}


class NeuralNetworkGrowthExample(PlotExample):

    primary = BITROOT_PALETTE['primary']
    tertiary = BITROOT_PALETTE['tertiary']
    light_gray = BITROOT_PALETTE['grid']

    def main(self):
        years = [2012, 2014, 2018, 2020]
        models = ["AlexNet", "VGG-16", "BERT", "GPT-3"]
        parameters = [60e6, 138e6, 340e6, 175e9]

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"neural_network_growth_line_log{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(10, 6), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            ax.plot(years, parameters, marker='o', color=self.primary, linewidth=2.5, markersize=7)
            ax.fill_between(years, parameters, color=to_rgba(self.primary, alpha=0.18))
            for i, txt in enumerate(models):
                ax.text(years[i], parameters[i], txt, fontsize=10, ha='right', color=BITROOT_PALETTE['text'])

            ax.set_yscale('log')

            ax.set_title(labels['title'], fontsize=14, color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels['xlabel'], color=BITROOT_PALETTE['text'])
            ax.set_xlim(min(years), max(years))
            ax.set_ylabel(labels['ylabel'], color=BITROOT_PALETTE['text'])

            apply_bitroot_style(ax)
            ax.grid(True, color=self.light_gray)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

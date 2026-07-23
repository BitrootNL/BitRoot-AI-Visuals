import numpy as np
import matplotlib.pyplot as plt

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Illustration of Noise in Data",
        "xlabel": "X Values",
        "ylabel": "Y Values",
        "true_label": "True Function (sin(x))",
        "noisy_label": "Noisy Observations",
    },
    "nl": {
        "title": "Illustratie van ruis in gegevens",
        "xlabel": "X-waarden",
        "ylabel": "Y-waarden",
        "true_label": "Werkelijke functie (sin(x))",
        "noisy_label": "Ruiswaarnemingen",
    },
}


class NoiseIllustration(PlotExample):

    primary: str = BITROOT_PALETTE['primary']
    tertiary: str = BITROOT_PALETTE['tertiary']

    def main(self) -> None:
        x = np.linspace(0, 10, 100)
        y_actual = np.sin(x)
        noise = np.random.normal(0, 0.3, size=x.shape)
        y_noisy = y_actual + noise

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"noisy_data_example{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(8, 5), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            ax.plot(x, y_actual, label=labels["true_label"], color=self.primary, linewidth=2)
            ax.scatter(x, y_noisy, label=labels["noisy_label"], color=self.tertiary, alpha=0.6)

            ax.set_xlabel(labels["xlabel"], color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels["ylabel"], color=BITROOT_PALETTE['text'])
            ax.set_title(labels["title"], color=BITROOT_PALETTE['text'])
            ax.legend()

            apply_bitroot_style(ax)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

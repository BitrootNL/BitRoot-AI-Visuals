import matplotlib.pyplot as plt
import numpy as np

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, output_path

TEXT_BY_LOCALE = {
    "en": {
        "title": "Subword Tokenization Process",
        "tokens": ["Tok", "en", "ization", "is", "es", "sen",
                   "tial", "for", "NLP", "mod", "els", "!"],
    },
    "nl": {
        "title": "Subwoord-tokenisatieproces",
        "tokens": ["Tok", "enis", "atie", "is", "ess", "en",
                   "ti", "eel", "voor", "NLP", "mod", "ellen", "!"],
    },
}


class TokenizationExample(PlotExample):

    def main(self):
        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            subword_tokens = labels["tokens"]
            x_positions = np.arange(len(subword_tokens))
            fname = f"tokenization_example{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(12, 3),
                                   facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            ax.scatter(x_positions, [1] * len(subword_tokens),
                       color=BITROOT_PALETTE['primary'], s=120,
                       edgecolor=BITROOT_PALETTE['text'], linewidth=0.5,
                       zorder=3)

            for i, token in enumerate(subword_tokens):
                ax.text(x_positions[i], 1.06, token, ha='center',
                        fontsize=11, fontweight='bold',
                        color=BITROOT_PALETTE['text'])

            for i in range(len(subword_tokens) - 1):
                ax.annotate('', xy=(x_positions[i+1] - 0.1, 1),
                            xytext=(x_positions[i] + 0.1, 1),
                            arrowprops=dict(arrowstyle='->',
                                            color=BITROOT_PALETTE['secondary_text'],
                                            lw=1.2))

            ax.set_xticks([])
            ax.set_yticks([])
            ax.set_title(labels["title"], fontsize=14, fontweight='bold',
                         color=BITROOT_PALETTE['text'], pad=10)
            ax.set_ylim(0.75, 1.25)
            ax.grid(False)
            for spine in ax.spines.values():
                spine.set_visible(False)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.15)
            plt.close(fig)

if __name__ == "__main__":
    TokenizationExample().main()

"""
Illustrates subword tokenization by displaying a sentence broken into
subword tokens as a connected scatter-point row.

Figures
-------
- ``tokenization.png`` / ``_NL.png`` — scatter row of subword tokens

Configuration
-------------
``CCPlots/plot_configs/tokenization.json``
"""
import numpy as np

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE


class Tokenization(PlotExample):

    CONFIG_KEY = "tokenization"

    def main(self):
        for _locale, labels, suffix in self.iter_locales():
            subword_tokens = labels["tokens"]
            x_positions = np.arange(len(subword_tokens))

            fig, ax = self.create_figure()

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

            self.save_figure(fig, "default", suffix=suffix)


if __name__ == "__main__":
    Tokenization().main()

"""
Schematic diagram of a single perceptron showing inputs, weights, bias, and
binary output.

Figures
-------
- ``perceptron_schematic.png`` / ``_NL.png`` — annotated perceptron schematic

Configuration
-------------
``CCPlots/plot_configs/perceptron.json``
"""
from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE


class Perceptron(PlotExample):

    CONFIG_KEY = "perceptron"

    def main(self) -> None:
        import matplotlib.patches as patches

        inputs = ['x1', 'x2', 'x3']
        weights = ['w1', 'w2', 'w3']
        input_positions = [6.5, 5.0, 3.5]

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()
            ax.set_xlim(0, 10)
            ax.set_ylim(0, 10)
            ax.axis('off')

            for i, (x, w, y) in enumerate(zip(inputs, weights, input_positions)):
                ax.annotate(x, (1, y), fontsize=12, ha='right', color=BITROOT_PALETTE['text'])
                ax.annotate(w, (2.2, y + 0.4), fontsize=10, ha='left', color=BITROOT_PALETTE['secondary_text'])
                ax.arrow(1.2, y, 2.3, 5 - y, head_width=0.1, head_length=0.2,
                         fc=BITROOT_PALETTE['text'], ec=BITROOT_PALETTE['text'],
                         length_includes_head=True)

            circle = patches.Circle((4.5, 5), 1.2,
                                    edgecolor=BITROOT_PALETTE['text'],
                                    facecolor=BITROOT_PALETTE['secondary'], lw=2)
            ax.add_patch(circle)
            ax.text(4.5, 5.4, r'$\sum (w_i x_i) + b$', fontsize=12,
                    ha='center', color=BITROOT_PALETTE['white'])
            ax.text(4.5, 4.3, labels['activation'], fontsize=10,
                    ha='center', color=BITROOT_PALETTE['white'])

            ax.arrow(5.7, 5, 2.5, 0, head_width=0.1, head_length=0.2,
                     fc=BITROOT_PALETTE['text'], ec=BITROOT_PALETTE['text'],
                     length_includes_head=True)
            ax.text(8.5, 5, labels['output'], fontsize=12, ha='left', color=BITROOT_PALETTE['text'])

            self.save_figure(fig, "default", suffix=suffix)


if __name__ == "__main__":
    Perceptron().main()

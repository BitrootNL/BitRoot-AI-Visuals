import matplotlib.colors as mcolors
import matplotlib.pyplot as plt

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


class LLMPredictExample(PlotExample):

    output_file = "llm_predict_next.png"

    @staticmethod
    def _probability_color(probability: float) -> str:
        """Return a primary-based shade where higher probability is darker."""
        base = mcolors.to_rgb(BITROOT_PALETTE["primary"])
        dark = mcolors.to_rgb(BITROOT_PALETTE["secondary"])
        blend = 0.05 + 0.95 * probability
        blended = tuple((1 - blend) * base[i] + blend * dark[i] for i in range(3))
        return mcolors.to_hex(blended)

    def main(self):
        # Re-import necessary libraries after execution state reset
        import matplotlib.pyplot as plt

        # Example sentence leading to next-word prediction
        prompt = "The cat sat on the"

        # Simulated probability distribution for the next word
        next_word_probs = {
            "mat": 0.5,
            "floor": 0.2,
            "chair": 0.15,
            "roof": 0.1,
            "dog": 0.05
        }

        # Extract words and their probabilities
        words = list(next_word_probs.keys())
        probabilities = list(next_word_probs.values())
        bar_colors = [self._probability_color(probability) for probability in probabilities]

        # Create bar chart
        plt.figure(figsize=(6, 4), facecolor=BITROOT_PALETTE["background"])
        ax = plt.gca()
        ax.set_facecolor(BITROOT_PALETTE["background"])
        ax.bar(words, probabilities, color=bar_colors, edgecolor=BITROOT_PALETTE["text"], linewidth=0.6)

        # Formatting the chart
        plt.ylim(0, 1)
        plt.ylabel("Probability", color=BITROOT_PALETTE["text"])
        plt.xlabel("Predicted Next Word", color=BITROOT_PALETTE["text"])
        plt.title(f"Predicting the Next Word for: '{prompt}'", color=BITROOT_PALETTE["text"], pad=10)
        apply_bitroot_style(ax)
        plt.tight_layout(pad=1.2)

        # Display the chart
        plt.savefig(output_path(self.output_file), bbox_inches="tight", pad_inches=0.1)

if __name__ == "__main__":
    LLMPredictExample().main()
"""
Bar chart of next-word probabilities predicted by an LLM for a partial
prompt. Bar colour intensity encodes the probability (darker = higher).

Figures
-------
- ``llm_predict_next.png`` / ``_NL.png`` — probability bar chart

Configuration
-------------
``CCPlots/plot_configs/llm_predict.json``
"""
from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, probability_color


class LLMPredict(PlotExample):

    CONFIG_KEY = "llm_predict"

    def main(self):
        next_word_probs = {
            "mat": 0.5,
            "floor": 0.2,
            "chair": 0.15,
            "roof": 0.1,
            "dog": 0.05,
        }

        words = list(next_word_probs.keys())
        probabilities = list(next_word_probs.values())

        for _locale, labels, suffix in self.iter_locales():
            bar_colors = [probability_color(p, "primary_pale", "primary")
                          for p in probabilities]
            prompt = labels["prompt"]

            fig, ax = self.create_figure()
            ax.bar(range(len(words)), probabilities, color=bar_colors,
                   edgecolor=BITROOT_PALETTE["text"], linewidth=0.7,
                   tick_label=labels["words"])

            ax.set_ylim(0, 1)
            ax.set_ylabel(labels["ylabel"], color=BITROOT_PALETTE["text"])
            ax.set_xlabel(labels["xlabel"], color=BITROOT_PALETTE["text"])
            title = labels["title"].format(prompt=prompt)
            ax.set_title(title, color=BITROOT_PALETTE["text"], pad=10)
            self.apply_style(ax)

            self.save_figure(fig, "default", suffix=suffix)


if __name__ == "__main__":
    LLMPredict().main()

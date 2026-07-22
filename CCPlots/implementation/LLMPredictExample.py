import matplotlib.pyplot as plt

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path, probability_color


TEXT_BY_LOCALE = {
    "en": {
        "title": "Predicting the Next Word for: '{prompt}'",
        "ylabel": "Probability",
        "xlabel": "Predicted Next Word",
        "prompt": "The cat sat on the",
        "words": ["mat", "floor", "chair", "roof", "dog"],
    },
    "nl": {
        "title": "Volgende woord voorspellen voor: '{prompt}'",
        "ylabel": "Kans",
        "xlabel": "Voorspeld volgend woord",
        "prompt": "De kat zat op de",
        "words": ["mat", "vloer", "stoel", "dak", "hond"],
    },
}


class LLMPredictExample(PlotExample):

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

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"llm_predict_next{'_NL' if locale == 'nl' else ''}.png"
            bar_colors = [probability_color(p, "primary_pale", "primary")
                          for p in probabilities]
            prompt = labels["prompt"]

            fig, ax = plt.subplots(figsize=(6, 4),
                                   facecolor=BITROOT_PALETTE["background"])
            ax.set_facecolor(BITROOT_PALETTE["background"])
            ax.bar(range(len(words)), probabilities, color=bar_colors,
                   edgecolor=BITROOT_PALETTE["text"], linewidth=0.7,
                   tick_label=labels["words"])

            ax.set_ylim(0, 1)
            ax.set_ylabel(labels["ylabel"], color=BITROOT_PALETTE["text"])
            ax.set_xlabel(labels["xlabel"], color=BITROOT_PALETTE["text"])
            title = labels["title"].format(prompt=prompt)
            ax.set_title(title, color=BITROOT_PALETTE["text"], pad=10)
            apply_bitroot_style(ax)

            fig.savefig(output_path(fname), bbox_inches="tight",
                        pad_inches=0.1)
            plt.close(fig)


if __name__ == "__main__":
    LLMPredictExample().main()
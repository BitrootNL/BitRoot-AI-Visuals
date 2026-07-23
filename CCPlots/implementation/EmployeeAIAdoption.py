import matplotlib.pyplot as plt

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path, probability_color

TEXT_BY_LOCALE = {
    "en": {
        "title": "Impact of AI on Work Experience (% of employees agreeing)",
        "ylabel": "Percentage",
        "categories": ["Time saved", "Focus improved", "Creativity boosted", "More enjoyment"],
    },
    "nl": {
        "title": "Impact van AI op werkervaring (% van de medewerkers eens)",
        "ylabel": "Percentage",
        "categories": ["Tijd bespaard", "Focus verbeterd", "Creativiteit verhoogd", "Meer werkplezier"],
    },
}

class EmployeeAIAdoption(PlotExample):

    def main(self):
        values = [90, 85, 84, 83]

        for locale, labels in (("nl", TEXT_BY_LOCALE["nl"]), ("en", TEXT_BY_LOCALE["en"])):
            fname = f"employee_ai_adoption{'_NL' if locale == 'nl' else ''}.png"
            categories = labels["categories"]

            n = len(values)
            bar_colors = [probability_color(i / (n - 1) if n > 1 else 0,
                                            "primary", "primary_pale")
                          for i in range(n)]

            fig, ax = plt.subplots(figsize=(10, 5),
                                   facecolor=BITROOT_PALETTE["background"])
            ax.set_facecolor(BITROOT_PALETTE["background"])
            ax.bar(categories, values, color=bar_colors,
                   edgecolor=BITROOT_PALETTE["text"], linewidth=0.6)

            ax.set_ylim(0, 100)
            ax.set_ylabel(labels["ylabel"], color=BITROOT_PALETTE["text"])
            ax.set_title(labels["title"], color=BITROOT_PALETTE["text"], pad=10)
            apply_bitroot_style(ax)

            fig.savefig(output_path(fname), bbox_inches="tight", pad_inches=0.1)
            plt.close(fig)


if __name__ == '__main__':
    EmployeeAIAdoption().main()
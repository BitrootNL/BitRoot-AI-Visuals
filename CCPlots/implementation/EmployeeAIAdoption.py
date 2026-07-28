"""
Bar chart measuring employee agreement with four AI-impact statements
(Time saved, Focus improved, Creativity boosted, More enjoyment).
Bar colour uses a primary-pale gradient to encode the value magnitude.

Figures
-------
- ``employee_ai_adoption.png`` / ``_NL.png`` — horizontal bar chart

Configuration
-------------
``CCPlots/plot_configs/employee_ai_adoption.json``
"""
from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, probability_color


class EmployeeAIAdoption(PlotExample):

    CONFIG_KEY = "employee_ai_adoption"

    def main(self):
        values = [90, 85, 84, 83]

        for _locale, labels, suffix in self.iter_locales():
            categories = labels["categories"]

            n = len(values)
            bar_colors = [probability_color(i / (n - 1) if n > 1 else 0,
                                            "primary", "primary_pale")
                          for i in range(n)]

            fig, ax = self.create_figure()
            ax.bar(categories, values, color=bar_colors,
                   edgecolor=BITROOT_PALETTE["text"], linewidth=0.6)

            ax.set_ylim(0, 100)
            ax.set_ylabel(labels["ylabel"], color=BITROOT_PALETTE["text"])
            ax.set_title(labels["title"], color=BITROOT_PALETTE["text"], pad=10)
            self.apply_style(ax)

            self.save_figure(fig, "default", suffix=suffix)


if __name__ == '__main__':
    EmployeeAIAdoption().main()

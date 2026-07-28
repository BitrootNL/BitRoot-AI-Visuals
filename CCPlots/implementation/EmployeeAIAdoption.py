"""
Bar chart measuring employee agreement with four AI-impact statements
(Time saved, Focus improved, Creativity boosted, More enjoyment).
Bar colour uses a primary-pale gradient to encode the value magnitude.

Figures
-------
- ``employee_ai_adoption.png`` / ``_NL.png`` — horizontal bar chart
"""
from CCPlots.PlotExample import PlotExample
from matplotlib.colors import LinearSegmentedColormap


class EmployeeAIAdoption(PlotExample):

    # CCPlots/plot_configs/employee_ai_adoption.json
    CONFIG_KEY = "employee_ai_adoption"

    def main(self):
        values = [90, 85, 84, 83]

        for _locale, labels, suffix in self.iter_locales():
            categories = labels["categories"]

            n = len(values)
            cmap = LinearSegmentedColormap.from_list(
                "adoption",
                [self.resolve_color('bar_gradient_start'),
                 self.resolve_color('bar_gradient_end')])
            bar_colors = [cmap(i / (n - 1)) for i in range(n)]

            fig, ax = self.create_figure()
            ax.bar(categories, values, color=bar_colors,
                   edgecolor=self.resolve_color('bar_edge'), linewidth=0.6)

            ax.set_ylim(0, 100)
            self.apply_labels(ax, ylabel=labels["ylabel"], title=labels["title"])
            self.apply_style(ax)

            self.save_figure(fig, "default", suffix=suffix)


if __name__ == '__main__':
    EmployeeAIAdoption().main()

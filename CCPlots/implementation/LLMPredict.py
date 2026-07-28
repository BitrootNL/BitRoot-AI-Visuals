"""
Bar chart of next-word probabilities predicted by an LLM for a partial
prompt. Bar colour intensity encodes the probability (darker = higher).

Figures
-------
- ``llm_predict_next.png`` / ``_NL.png`` — probability bar chart
"""
from CCPlots.PlotExample import PlotExample
from matplotlib.colors import LinearSegmentedColormap


class LLMPredict(PlotExample):

    # CCPlots/plot_configs/llm_predict.json
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
            cmap = LinearSegmentedColormap.from_list(
                "predict",
                [self.resolve_color('bar_gradient_start'),
                 self.resolve_color('bar_gradient_end')])
            bar_colors = [cmap(p) for p in probabilities]
            prompt = labels["prompt"]

            fig, ax = self.create_figure()
            ax.bar(range(len(words)), probabilities, color=bar_colors,
                   edgecolor=self.resolve_color('bar_edge'), linewidth=0.7,
                   tick_label=labels["words"])

            ax.set_ylim(0, 1)
            title = labels["title"].format(prompt=prompt)
            self.apply_labels(ax, title=title, xlabel=labels["xlabel"],
                              ylabel=labels["ylabel"])
            self.apply_style(ax)

            self.save_figure(fig, "default", suffix=suffix)


if __name__ == "__main__":
    LLMPredict().main()

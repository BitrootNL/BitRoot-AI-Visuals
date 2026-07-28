"""
Demonstrates the concept of noise in data by plotting a clean sin(x) curve
alongside noisy observations sampled from a Gaussian distribution around it.

Figures
-------
- ``noisy_data.png`` / ``_NL.png`` — clean curve + noisy scatter
"""
import numpy as np

from CCPlots.PlotExample import PlotExample


class NoisyData(PlotExample):

    # CCPlots/plot_configs/noisy_data.json
    CONFIG_KEY = "noisy_data"

    def main(self) -> None:
        x = np.linspace(0, 10, 100)
        y_actual = np.sin(x)
        noise = np.random.normal(0, 0.3, size=x.shape)
        y_noisy = y_actual + noise

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            ax.plot(x, y_actual, label=labels["true_label"], color=self.resolve_color('true_curve'), linewidth=2)
            ax.scatter(x, y_noisy, label=labels["noisy_label"], color=self.resolve_color('noisy_dots'), alpha=0.6)

            self.apply_labels(ax, title=labels["title"], xlabel=labels["xlabel"],
                              ylabel=labels["ylabel"])
            ax.legend()

            self.apply_style(ax)
            self.save_figure(fig, "default", suffix=suffix)


if __name__ == "__main__":
    NoisyData().main()

"""
Two-panel comparison of continuous age data (histogram) versus discrete
age-group categories (bar chart), illustrating the binning concept.

Figures
-------
- ``continuous_discrete.png`` / ``_NL.png`` — histogram + bar chart
"""
import numpy as np
import pandas as pd

from CCPlots.PlotExample import PlotExample
from CCPlots.config import GLOBAL_RANDOM_STATE


class ContinuousDiscrete(PlotExample):

    # CCPlots/plot_configs/continuous_discrete.json
    CONFIG_KEY = "continuous_discrete"

    def main(self) -> None:
        np.random.seed(GLOBAL_RANDOM_STATE)
        ages = np.concatenate([
            np.random.normal(loc=35, scale=10, size=450),
            np.random.normal(loc=75, scale=8, size=40),
            np.random.normal(loc=95, scale=3, size=10)
        ])
        ages = np.clip(ages, 0, 115)

        bins = [0, 18, 25, 35, 50, 65, 80, 100]

        for _locale, labels, suffix in self.iter_locales():
            age_bins = pd.cut(ages, bins=bins, labels=labels["bins_labels"], right=False)

            df = pd.DataFrame({
                'Age': ages,
                'Age Group': age_bins
            })

            fig, axs = self.create_figure(ncols=2)

            cat_order = labels["bins_labels"]
            cat_counts = df['Age Group'].value_counts()
            cat_vals = [cat_counts.get(c, 0) for c in cat_order]
            bar_positions = range(len(cat_order))
            axs[1].bar(bar_positions, cat_vals, color=self.resolve_color('bar_fill'), edgecolor=self.resolve_color('bar_fill'))
            axs[1].set_xticks(list(bar_positions))
            axs[1].set_xticklabels(cat_order)
            self.apply_labels(axs[1], title=labels["cat_title"],
                              xlabel=labels["cat_xlabel"], ylabel=labels["cat_ylabel"])

            axs[0].hist(df['Age'], bins=30, density=True, color=self.resolve_color('hist_fill'), alpha=0.7)
            self.apply_labels(axs[0], title=labels["cont_title"],
                              xlabel=labels["cont_xlabel"], ylabel=labels["cont_ylabel"])

            for ax in axs:
                self.apply_style(ax)

            self.save_figure(fig, "default", suffix=suffix)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "cat_title": "Ages divided into age categories",
        "cat_xlabel": "Age group",
        "cat_ylabel": "Count",
        "cont_title": "Age distribution in real life",
        "cont_xlabel": "Actual age",
        "cont_ylabel": "Count",
        "bins_labels": ['<18', '18\u201324', '25\u201334', '35\u201349', '50\u201364', '65\u201379', '80+'],
    },
    "nl": {
        "cat_title": "Leeftijden verdeeld in leeftijdscategorie\u00ebn",
        "cat_xlabel": "Leeftijdsgroep",
        "cat_ylabel": "Aantal",
        "cont_title": "Leeftijdsverdeling in het echt",
        "cont_xlabel": "Werkelijke leeftijd",
        "cont_ylabel": "Aantal",
        "bins_labels": ['<18', '18\u201324', '25\u201334', '35\u201349', '50\u201364', '65\u201379', '80+'],
    },
}


class ContinuousDiscreteExample(PlotExample):

    primary = BITROOT_PALETTE['primary']
    tertiary = BITROOT_PALETTE['tertiary']

    def main(self) -> None:
        np.random.seed(42)
        ages = np.concatenate([
            np.random.normal(loc=35, scale=10, size=450),
            np.random.normal(loc=75, scale=8, size=40),
            np.random.normal(loc=95, scale=3, size=10)
        ])
        ages = np.clip(ages, 0, 115)

        bins = [0, 18, 25, 35, 50, 65, 80, 100]

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"continuous_discrete_example{'_NL' if locale == 'nl' else ''}.png"

            age_bins = pd.cut(ages, bins=bins, labels=labels["bins_labels"], right=False)

            df = pd.DataFrame({
                'Age': ages,
                'Age Group': age_bins
            })

            fig, axs = plt.subplots(1, 2, figsize=(14, 5),
                                    facecolor=BITROOT_PALETTE['background'])
            fig.patch.set_facecolor(BITROOT_PALETTE['background'])

            cat_order = labels["bins_labels"]
            cat_counts = df['Age Group'].value_counts()
            cat_vals = [cat_counts.get(c, 0) for c in cat_order]
            bar_positions = range(len(cat_order))
            axs[1].bar(bar_positions, cat_vals, color=self.primary, edgecolor=self.primary)
            axs[1].set_xticks(list(bar_positions))
            axs[1].set_xticklabels(cat_order)
            axs[1].set_title(labels["cat_title"], color=BITROOT_PALETTE['text'])
            axs[1].set_xlabel(labels["cat_xlabel"], color=BITROOT_PALETTE['text'])
            axs[1].set_ylabel(labels["cat_ylabel"], color=BITROOT_PALETTE['text'])

            axs[0].hist(df['Age'], bins=30, density=True, color=self.primary, alpha=0.7)
            axs[0].set_title(labels["cont_title"], color=BITROOT_PALETTE['text'])
            axs[0].set_xlabel(labels["cont_xlabel"], color=BITROOT_PALETTE['text'])
            axs[0].set_ylabel(labels["cont_ylabel"], color=BITROOT_PALETTE['text'])

            for ax in axs:
                apply_bitroot_style(ax)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

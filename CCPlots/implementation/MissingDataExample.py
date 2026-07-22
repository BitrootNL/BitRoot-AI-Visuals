import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import fetch_openml

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path

TEXT_BY_LOCALE = {
    "en": {
        "title": "Examples of missing data in the Adult data set",
        "col_age": "Age",
        "col_workclass": "Workclass",
        "col_sex": "Sex",
        "col_education": "Education",
        "na_label": "?",
        "note": "Rows with naturally occurring missing values",
    },
    "nl": {
        "title": "Voorbeelden van ontbrekende gegevens in de Adult-dataset",
        "col_age": "Leeftijd",
        "col_workclass": "Werkklasse",
        "col_sex": "Geslacht",
        "col_education": "Opleiding",
        "na_label": "?",
        "note": "Rijen met van nature ontbrekende waarden",
    },
}


class MissingDataExample(PlotExample):

    def main(self) -> None:
        dataset = fetch_openml(data_id=1590, as_frame=True)
        df: pd.DataFrame = dataset.frame

        df_missing = df[df.isnull().any(axis=1)]
        if df_missing.empty:
            return

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"naturally_missing_data_table{'_NL' if locale == 'nl' else ''}.png"
            display = df_missing.head(10)[["age", "workclass", "sex", "education"]].copy()
            display.columns = [labels["col_age"], labels["col_workclass"],
                               labels["col_sex"], labels["col_education"]]

            n_rows, n_cols = display.shape
            fig = plt.figure(figsize=(10, 0.35 * n_rows + 0.6),
                             facecolor=BITROOT_PALETTE['background'])
            ax = fig.add_axes([0, 0, 1, 1])
            ax.axis('off')

            cell_text = []
            cell_colors = []
            for row_idx in range(n_rows):
                row_vals = []
                row_colors = []
                bg = BITROOT_PALETTE['white'] if row_idx % 2 == 0 else BITROOT_PALETTE['background']
                for col_idx in range(n_cols):
                    val = display.iloc[row_idx, col_idx]
                    if pd.isna(val):
                        row_vals.append(labels["na_label"])
                    else:
                        row_vals.append(str(val))
                    row_colors.append(bg)
                cell_text.append(row_vals)
                cell_colors.append(row_colors)

            header_color = BITROOT_PALETTE['primary']
            header_text_color = BITROOT_PALETTE['white']

            table = ax.table(
                cellText=cell_text,
                colLabels=list(display.columns),
                cellColours=cell_colors,
                colColours=[header_color] * n_cols,
                cellLoc='left',
                loc='center',
            )

            table.auto_set_font_size(False)
            table.set_fontsize(10)

            for key, cell in table.get_celld().items():
                row, col = key
                cell.set_edgecolor(BITROOT_PALETTE['grid'])
                cell.set_linewidth(0.5)
                if row == 0:
                    cell.set_text_props(color=header_text_color, fontweight='bold')
                    cell.set_height(0.06)
                else:
                    cell.set_text_props(color=BITROOT_PALETTE['text'])
                    cell.set_height(0.045)

            table.scale(1, 1.4)

            ax.set_title(labels["title"], fontsize=13, color=BITROOT_PALETTE['text'],
                         fontweight='bold', pad=8)

            ax.text(0.5, -0.06, labels["note"], fontsize=8,
                    color=BITROOT_PALETTE['secondary_text'],
                    ha='center', va='top', transform=ax.transAxes)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.08,
                        dpi=150)
            plt.close(fig)


if __name__ == "__main__":
    MissingDataExample().main()
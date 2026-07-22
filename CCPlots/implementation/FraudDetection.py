import numpy as np
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path

TEXT_BY_LOCALE = {
    "en": {
        "title": "Decision Boundary for Fraud Detection",
        "xlabel": "Feature 1 (standardized)",
        "ylabel": "Feature 2 (standardized)",
        "legend_title": "Classes",
        "legend_no_fraud": "No Fraud",
        "legend_fraud": "Fraud",
    },
    "nl": {
        "title": "Beslissingsgrens voor Fraudedetectie",
        "xlabel": "Kenmerk 1 (gestandaardiseerd)",
        "ylabel": "Kenmerk 2 (gestandaardiseerd)",
        "legend_title": "Klassen",
        "legend_no_fraud": "Geen Fraude",
        "legend_fraud": "Fraude",
    },
}


class FraudDetection(PlotExample):

    fraud_cmap = mcolors.ListedColormap([
        BITROOT_PALETTE["primary"],
        BITROOT_PALETTE["highlight"],
    ])

    def main(self) -> None:
        X, y = make_classification(
            n_samples=800,
            n_features=2,
            n_informative=2,
            n_redundant=0,
            n_clusters_per_class=1,
            weights=[0.9, 0.1],
            class_sep=1.8,
            random_state=42
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, stratify=y, random_state=42
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = LogisticRegression(class_weight="balanced", random_state=42)
        model.fit(X_train_scaled, y_train)

        x_min, x_max = X_train_scaled[:, 0].min() - 1, X_train_scaled[:, 0].max() + 1
        y_min, y_max = X_train_scaled[:, 1].min() - 1, X_train_scaled[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 500),
                             np.linspace(y_min, y_max, 500))

        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"decision_boundary_fraud{'_NL' if locale == 'nl' else ''}.png"
            fig, ax = plt.subplots(figsize=(7, 5), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            boundary_cmap = mcolors.LinearSegmentedColormap.from_list(
                "fraud_boundary",
                [BITROOT_PALETTE["primary_soft"], BITROOT_PALETTE["highlight"]],
                N=256,
            )
            ax.contourf(xx, yy, Z, alpha=0.25, cmap=boundary_cmap)

            scatter = ax.scatter(
                X_train_scaled[:, 0],
                X_train_scaled[:, 1],
                c=y_train,
                edgecolor=BITROOT_PALETTE['secondary_text'],
                linewidth=0.5,
                cmap=self.fraud_cmap,
                s=40,
            )

            handles, legend_labels = scatter.legend_elements()
            ax.legend(handles,
                      [labels["legend_no_fraud"], labels["legend_fraud"]],
                      title=labels["legend_title"],
                      frameon=False, fontsize=10)
            ax.set_title(labels["title"], fontsize=14, color=BITROOT_PALETTE['text'], pad=10)
            ax.set_xlabel(labels["xlabel"], fontsize=13, color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels["ylabel"], fontsize=13, color=BITROOT_PALETTE['text'])
            apply_bitroot_style(ax)
            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

if __name__ == "__main__":
    FraudDetection().main()
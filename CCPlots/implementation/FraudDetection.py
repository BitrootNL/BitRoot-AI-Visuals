"""
Decision boundary plot for a fraud-detection classifier trained on an
imbalanced dataset (90 % legitimate, 10 % fraudulent). Uses logistic
regression with balanced class weights and standardised features.

Figures
-------
- ``fraud_detection_boundary.png`` / ``_NL.png`` — decision boundary scatter

Configuration
-------------
``CCPlots/plot_configs/fraud_detection.json``
"""
import matplotlib.colors as mcolors
import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, GLOBAL_RANDOM_STATE


class FraudDetection(PlotExample):

    CONFIG_KEY = "fraud_detection"

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
            random_state=GLOBAL_RANDOM_STATE
        )

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.25, stratify=y, random_state=42
        )

        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        #X_test_scaled = scaler.transform(X_test)

        model = LogisticRegression(class_weight="balanced", random_state=GLOBAL_RANDOM_STATE, max_iter=1000)
        model.fit(X_train_scaled, y_train)

        x_min, x_max = X_train_scaled[:, 0].min() - 1, X_train_scaled[:, 0].max() + 1
        y_min, y_max = X_train_scaled[:, 1].min() - 1, X_train_scaled[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 500),
                             np.linspace(y_min, y_max, 500))

        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

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
            self.apply_style(ax)
            self.save_figure(fig, "default", suffix=suffix)


if __name__ == "__main__":
    FraudDetection().main()

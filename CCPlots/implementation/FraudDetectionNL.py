import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, CMAP_CONTRAST, output_path


class FraudDetectionNL(PlotExample):
    def main(self) -> None:
        # Maak een eenvoudige 2D dataset voor decision boundary-visualisatie
        X, y = make_classification(
            n_samples=800,
            n_features=2,            # Alleen 2 features voor visualisatie
            n_informative=2,
            n_redundant=0,
            n_clusters_per_class=1,
            weights=[0.9, 0.1],      # 10% fraude
            class_sep=1.8,
            random_state=42
        )

        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

        # Logistische regressie model
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        model = LogisticRegression(class_weight="balanced", random_state=42)
        model.fit(X_train_scaled, y_train)

        # Genereer meshgrid voor decision boundary
        x_min, x_max = X_train_scaled[:, 0].min() - 1, X_train_scaled[:, 0].max() + 1
        y_min, y_max = X_train_scaled[:, 1].min() - 1, X_train_scaled[:, 1].max() + 1
        xx, yy = np.meshgrid(np.linspace(x_min, x_max, 500),
                             np.linspace(y_min, y_max, 500))

        # Voorspellingen over het grid
        Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
        Z = Z.reshape(xx.shape)

        # Visualisatie
        fig, ax = plt.subplots(figsize=(7, 5), facecolor=BITROOT_PALETTE['background'])
        ax.set_facecolor(BITROOT_PALETTE['background'])

        # Decision boundary
        ax.contourf(xx, yy, Z, alpha=0.3, cmap=CMAP_CONTRAST)

        # Plot trainingsdata
        scatter = ax.scatter(
            X_train_scaled[:, 0],
            X_train_scaled[:, 1],
            c=y_train,
            edgecolor='k',
            cmap=CMAP_CONTRAST,
            s=40
        )

        # Labels en titel in het Nederlands
        handles, labels = scatter.legend_elements()
        ax.legend(handles, ["Geen Fraude", "Fraude"], title="Klassen")
        ax.set_title("Beslissingsgrens voor Fraudedetectie", fontsize=13, color=BITROOT_PALETTE['text'])
        ax.set_xlabel("Kenmerk 1 (gestandaardiseerd)", color=BITROOT_PALETTE['text'])
        ax.set_ylabel("Kenmerk 2 (gestandaardiseerd)", color=BITROOT_PALETTE['text'])

        fig.tight_layout()
        fig.savefig(output_path("decision_boundary_fraud_NL.png"))

if __name__ == "__main__":
    FraudDetectionNL().main()
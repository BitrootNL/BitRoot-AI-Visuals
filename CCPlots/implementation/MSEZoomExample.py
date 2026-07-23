import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.datasets import make_regression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Differences between predicted function and actual values",
        "xlabel": "X value (feature)",
        "ylabel": "Y value (prediction/actual)",
        "data_label": "Data points",
        "line_label": "Fitted line",
    },
    "nl": {
        "title": "Verschillen tussen voorspelde functie en werkelijke waarden",
        "xlabel": "X-waarde (kenmerk)",
        "ylabel": "Y-waarde (voorspelling/werkelijk)",
        "data_label": "Datapunten",
        "line_label": "Aangepaste lijn",
    },
}


class MSEZoomExample(PlotExample):

    primary = BITROOT_PALETTE['primary']
    secondary = BITROOT_PALETTE['secondary']
    tertiary = BITROOT_PALETTE['tertiary']
    light_gray = BITROOT_PALETTE['grid']

    y_pred = None

    def __init__(self, n_samples=100, learning_rate=0.01):
        self.n_samples = n_samples
        self.learning_rate = learning_rate

        self.X, self.y = make_regression(
            n_samples=self.n_samples,
            n_features=1,
            noise=15,
            random_state=42)

        self.model = SGDRegressor(
            max_iter=1,
            tol=None,
            learning_rate='constant',
            eta0=self.learning_rate,
            random_state=42
        )

    def main(self):
        self.train_one_iteration()
        self.plot_mse_zoom()

    def train_one_iteration(self):
        self.model.partial_fit(self.X, self.y)
        self.y_pred = self.model.predict(self.X)

    def plot_mse_zoom(self):
        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"mse_zoom_iteration{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(10, 6), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            ax.scatter(self.X, self.y, color=self.tertiary, label=labels['data_label'],
                       edgecolor=self.primary, linewidth=0.8, s=55, zorder=3)
            ax.plot(self.X, self.y_pred, color=self.primary, label=labels['line_label'],
                    linewidth=2.5, zorder=2)

            for i in range(len(self.X)):
                ax.plot([self.X[i], self.X[i]], [self.y[i], self.y_pred[i]],
                        color=self.primary, linestyle='--', alpha=0.35, linewidth=1.0, zorder=1)

            ax.set_title(labels['title'], fontsize=16, color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels['xlabel'], fontsize=14, color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels['ylabel'], fontsize=14, color=BITROOT_PALETTE['text'])

            apply_bitroot_style(ax)
            ax.grid(True, color=self.light_gray)
            ax.legend()

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

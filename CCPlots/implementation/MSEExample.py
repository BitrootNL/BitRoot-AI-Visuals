import matplotlib.pyplot as plt
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import mean_squared_error
from sklearn.datasets import make_regression

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "MSE over Iterations",
        "xlabel": "Iteration",
        "ylabel": "Mean Squared Error",
    },
    "nl": {
        "title": "MSE over iteraties",
        "xlabel": "Iteratie",
        "ylabel": "Gemiddelde kwadratische fout",
    },
}


class MSEExample(PlotExample):
    primary = BITROOT_PALETTE['primary']
    light_gray = BITROOT_PALETTE['grid']

    def __init__(self, n_samples=100, iterations=50, learning_rate=0.01):
        self.n_samples = n_samples
        self.iterations = iterations
        self.learning_rate = learning_rate

        self.X, self.y = make_regression(n_samples=self.n_samples, n_features=1, noise=15, random_state=42)

        self.model = SGDRegressor(max_iter=1, tol=None, learning_rate='constant', eta0=self.learning_rate,
                                  random_state=42)

        self.mse_values = []

    def main(self):
        self.train_and_calculate_mse()
        self.plot_mse()

    def train_and_calculate_mse(self):
        for _ in range(self.iterations):
            self.model.partial_fit(self.X, self.y)
            y_pred = self.model.predict(self.X)
            mse = mean_squared_error(self.y, y_pred)
            self.mse_values.append(mse)

    def plot_mse(self):
        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"mse_over_iterations{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(10, 6), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

            ax.plot(range(1, self.iterations + 1), self.mse_values, color=self.primary, marker='o')
            ax.set_title(labels['title'], fontsize=16, color=BITROOT_PALETTE['text'])
            ax.set_xlabel(labels['xlabel'], fontsize=14, color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels['ylabel'], fontsize=14, color=BITROOT_PALETTE['text'])

            apply_bitroot_style(ax)
            ax.grid(True, color=self.light_gray)

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

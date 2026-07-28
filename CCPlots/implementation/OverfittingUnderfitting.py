"""
Two-panel comparison of underfitting (degree-2 polynomial, high bias) versus
overfitting (degree-11 polynomial, high variance) on a sine-wave dataset.
Each panel shows training/test MSE.

Figures
-------
- ``overfitting_underfitting.png`` / ``_NL.png`` — side-by-side under/over fit

Configuration
-------------
``CCPlots/plot_configs/overfitting_underfitting.json``
"""
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, GLOBAL_RANDOM_STATE


class OverfittingUnderfitting(PlotExample):

    CONFIG_KEY = "overfitting_underfitting"

    prediction_color = BITROOT_PALETTE['highlight']
    training_color = BITROOT_PALETTE['secondary']
    test_color = BITROOT_PALETTE['primary']

    light_gray = BITROOT_PALETTE['grid']

    def main(self):
        np.random.seed(GLOBAL_RANDOM_STATE)
        X = np.sort(np.random.rand(40, 1) * 10, axis=0)
        y = np.sin(X).ravel() + np.random.normal(0, 0.2, X.shape[0])

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=GLOBAL_RANDOM_STATE)

        poly_under = PolynomialFeatures(degree=2)
        poly_over = PolynomialFeatures(degree=11)

        X_train_under = poly_under.fit_transform(X_train)
        X_test_under = poly_under.transform(X_test)

        X_train_over = poly_over.fit_transform(X_train)
        X_test_over = poly_over.transform(X_test)

        model_under = LinearRegression().fit(X_train_under, y_train)
        model_over = LinearRegression().fit(X_train_over, y_train)

        X_range = np.linspace(X.min(), X.max(), 500).reshape(-1, 1)
        X_range_under = poly_under.transform(X_range)
        X_range_over = poly_over.transform(X_range)

        y_range_pred_under = model_under.predict(X_range_under)
        y_range_pred_over = model_over.predict(X_range_over)

        y_pred_under_train = model_under.predict(X_train_under)
        y_pred_under_test = model_under.predict(X_test_under)

        y_pred_over_train = model_over.predict(X_train_over)
        y_pred_over_test = model_over.predict(X_test_over)

        mse_under_train = mean_squared_error(y_train, y_pred_under_train)
        mse_under_test = mean_squared_error(y_test, y_pred_under_test)

        mse_over_train = mean_squared_error(y_train, y_pred_over_train)
        mse_over_test = mean_squared_error(y_test, y_pred_over_test)

        for _locale, labels, suffix in self.iter_locales():
            fig, (ax1, ax2) = self.create_figure(ncols=2)

            ax1.scatter(X_train, y_train, color=self.training_color, label=labels['train_label'])
            ax1.scatter(X_test, y_test, color=self.test_color, label=labels['test_label'])
            ax1.plot(X_range, y_range_pred_under, color=self.prediction_color, label=labels['under_label'])
            ax1.set_title(labels['under_title'].format(train_mse=mse_under_train, test_mse=mse_under_test),
                          color=BITROOT_PALETTE['text'])
            ax1.set_xlabel(labels['xlabel'], color=BITROOT_PALETTE['text'])
            ax1.set_ylabel(labels['ylabel'], color=BITROOT_PALETTE['text'])
            ax1.legend()
            ax1.grid(True, c=self.light_gray)
            self.apply_style(ax1)

            ax2.scatter(X_train, y_train, color=self.training_color, label=labels['train_label'])
            ax2.scatter(X_test, y_test, color=self.test_color, label=labels['test_label'])
            ax2.plot(X_range, y_range_pred_over, color=self.prediction_color, label=labels['over_label'])
            ax2.set_title(labels['over_title'].format(train_mse=mse_over_train, test_mse=mse_over_test),
                          color=BITROOT_PALETTE['text'])
            ax2.set_xlabel(labels['xlabel'], color=BITROOT_PALETTE['text'])
            ax2.set_ylabel(labels['ylabel'], color=BITROOT_PALETTE['text'])
            ax2.legend()
            ax2.grid(True, c=self.light_gray)
            self.apply_style(ax2)

            self.save_figure(fig, "default", suffix=suffix)

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from ..PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path

# Implement the noise illustration
class NoiseIllustration(PlotExample):

    primary: str = BITROOT_PALETTE['primary']
    tertiary: str = BITROOT_PALETTE['tertiary']

    def main(self) -> None:
        """ Generates and plots a noisy sine wave with the actual function """

        # Set seaborn style
        sns.set_style("whitegrid")

        # Generate x values
        x = np.linspace(0, 10, 100)

        # Generate actual function (sine wave)
        y_actual = np.sin(x)

        # Generate noisy data
        noise = np.random.normal(0, 0.3, size=x.shape)  # Adding Gaussian noise
        y_noisy = y_actual + noise

        # Create the plot
        plt.figure(figsize=(8, 5), facecolor=BITROOT_PALETTE['background'])
        plt.plot(x, y_actual, label="True Function (sin(x))", color=self.primary, linewidth=2)  # True function
        plt.scatter(x, y_noisy, label="Noisy Observations", color=self.tertiary, alpha=0.6)  # Noisy points

        # Labels and legend
        plt.xlabel("X Values", color=BITROOT_PALETTE['text'])
        plt.ylabel("Y Values", color=BITROOT_PALETTE['text'])
        plt.title("Illustration of Noise in Data", color=BITROOT_PALETTE['text'])
        plt.legend()

        ax = plt.gca()
        apply_bitroot_style(ax)
        plt.savefig(output_path("noisy_data_example.png"))


if __name__ == "__main__":
    NoiseIllustration().main()
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, CMAP_WHITE, output_path


class EvaluationMetricsExample(PlotExample):

    def main(self):
        # Define the confusion matrix values again
        conf_matrix = np.array([[50, 10],  # 50 True Negatives, 10 False Positives
                                [5, 35]])  # 5 False Negatives, 35 True Positives

        # Labels for the plot including counts
        group_labels = np.array([
            f"True Negative\n(Healthy correctly diagnosed)\n{conf_matrix[0, 0]}",
            f"False Positive\n(Healthy misdiagnosed as sick)\n{conf_matrix[0, 1]}",
            f"False Negative\n(Sick misdiagnosed as healthy)\n{conf_matrix[1, 0]}",
            f"True Positive\n(Sick correctly diagnosed)\n{conf_matrix[1, 1]}"
        ]).reshape(2, 2)

        # Create the heatmap
        plt.figure(figsize=(8, 6), facecolor=BITROOT_PALETTE['background'])
        ax = sns.heatmap(conf_matrix, annot=group_labels, fmt="", cmap=CMAP_WHITE, cbar=True,
                         xticklabels=["Predicted Healthy", "Predicted Sick"],
                         yticklabels=["Is Healthy", "Is Sick"])

        # Add labels and title
        plt.xlabel("Predicted Label", color=BITROOT_PALETTE['text'])
        plt.ylabel("Actual Label", color=BITROOT_PALETTE['text'])
        plt.title("Evaluating Results for Disease Diagnosis", color=BITROOT_PALETTE['text'])

        # Show the plot
        plt.savefig(output_path("confusion_matrix.png"))

if __name__ == "__main__":
    EvaluationMetricsExample().main()
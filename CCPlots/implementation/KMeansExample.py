"""
KMeansExample.py

This example creates an animation and stores the final clusters as determined
by the KMeans algorithm.
"""

from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, darken_color, output_path

CLUSTER_PALETTE = [
    BITROOT_PALETTE["primary"],
    BITROOT_PALETTE["secondary"],
    BITROOT_PALETTE["highlight"],
    darken_color(BITROOT_PALETTE["primary"]),
    darken_color(BITROOT_PALETTE["secondary"]),
    darken_color(BITROOT_PALETTE["highlight"]),
    darken_color(BITROOT_PALETTE["primary"], 0.4),
]


class KMeansExample(PlotExample):

    centers = None
    scatter = None
    legend = None

    def __init__(self, n_clusters=4, n_samples=300):
        self.n_clusters = n_clusters
        self.n_samples = n_samples
        self.X, self.y = make_blobs(
            n_samples=self.n_samples,
            centers=self.n_clusters,
            cluster_std=3.0,
            random_state=42)
        self.kmeans = KMeans(
            n_clusters=self.n_clusters,
            init='random',
            n_init=1,
            max_iter=1,
            algorithm='lloyd',
            random_state=42)

        self.cluster_colors = [CLUSTER_PALETTE[i % len(CLUSTER_PALETTE)]
                               for i in range(self.n_clusters)]

    def _make_legend(self, ax):
        patches = [
            mpatches.Patch(facecolor=self.cluster_colors[i],
                           edgecolor=BITROOT_PALETTE['text'],
                           linewidth=0.5,
                           label=f"Cluster {i + 1}")
            for i in range(self.n_clusters)
        ]
        patches.append(
            mpatches.Patch(facecolor='none', edgecolor='none', label=''))  # spacer
        patches.append(
            plt.Line2D([0], [0], marker='X', color=BITROOT_PALETTE['text'],
                       markerfacecolor=BITROOT_PALETTE['white'],
                       markeredgecolor=BITROOT_PALETTE['text'],
                       markersize=10, markeredgewidth=2, label='Centroid'))
        return ax.legend(handles=patches, title='Clusters', frameon=False,
                         fontsize=8, title_fontsize=9,
                         loc='upper right', ncol=2)

    def main(self):
        fig, ax = plt.subplots(figsize=(8, 6),
                               facecolor=BITROOT_PALETTE['background'])
        ax.set_xlim(-20, 20)
        ax.set_ylim(-20, 20)

        self.scatter = ax.scatter(self.X[:, 0], self.X[:, 1], s=30,
                                  c='grey', edgecolor=BITROOT_PALETTE['text'],
                                  linewidth=0.4)
        self.centers = ax.scatter([], [], s=200, marker='X',
                                  facecolor=BITROOT_PALETTE['white'],
                                  edgecolor=BITROOT_PALETTE['text'],
                                  linewidth=2)

        ax.set_title("KMeans Clustering: Determining Species",
                     fontsize=16, color=BITROOT_PALETTE['text'], pad=10)
        ax.set_xlabel("Height of a penguin",
                      fontsize=14, color=BITROOT_PALETTE['text'])
        ax.set_ylabel("Weight of a penguin",
                      fontsize=14, color=BITROOT_PALETTE['text'])

        self.legend = self._make_legend(ax)
        apply_bitroot_style(ax)

        ani = FuncAnimation(fig, self.update, frames=30,
                            init_func=self.init_func, interval=10,
                            repeat=False)
        ani.save(output_path(f"kmeans_animation_k{self.n_clusters}.gif"),
                 writer='pillow')

        fig.savefig(output_path(f"kmeans_clustering_k{self.n_clusters}.png"),
                    bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)

    def update(self, frame):
        self.kmeans.max_iter = frame + 1
        self.kmeans.fit(self.X)

        labels = self.kmeans.labels_
        scatter_colors = [self.cluster_colors[label] for label in labels]

        self.scatter.set_color(scatter_colors)
        self.scatter.set_edgecolor(BITROOT_PALETTE['text'])
        self.centers.set_offsets(self.kmeans.cluster_centers_)
        center_colors = [self.cluster_colors[i] for i in range(self.n_clusters)]
        self.centers.set_facecolor([BITROOT_PALETTE['white']] * self.n_clusters)
        self.centers.set_edgecolor(center_colors)
        self.centers.set_linewidth(2.5)
        return self.scatter, self.centers

    def init_func(self):
        self.scatter.set_offsets(self.X)
        return self.scatter, self.centers


if __name__ == "__main__":
    for k in (3, 4):
        KMeansExample(n_clusters=k).main()

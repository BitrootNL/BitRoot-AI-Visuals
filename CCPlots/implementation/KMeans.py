"""
Animated K-Means clustering showing cluster assignment and centroid movement
over 30 iterations. Also produces a static final-frame PNG. Runs for k = 3
and k = 4.

Figures
-------
- ``kmeans_animation_k{n_clusters}.gif`` / ``_NL.gif`` — animation
- ``kmeans_clustering_k{n_clusters}.png`` / ``_NL.png`` — final frame

Configuration
-------------
``CCPlots/plot_configs/kmeans.json``
"""
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from sklearn.cluster import KMeans as SKKMeans
from sklearn.datasets import make_blobs

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, GLOBAL_RANDOM_STATE, darken_color, output_path


CLUSTER_PALETTE = [
    BITROOT_PALETTE["primary"],
    BITROOT_PALETTE["secondary"],
    BITROOT_PALETTE["highlight"],
    darken_color(BITROOT_PALETTE["primary"]),
    darken_color(BITROOT_PALETTE["secondary"]),
    darken_color(BITROOT_PALETTE["highlight"]),
    darken_color(BITROOT_PALETTE["primary"], 0.4),
]


class KMeans(PlotExample):

    CONFIG_KEY = "kmeans"

    centers = None
    scatter = None
    legend = None

    def __init__(self, n_clusters=4, n_samples=200):
        self.n_clusters = n_clusters
        self.n_samples = n_samples
        self.X, self.y = make_blobs(
            n_samples=self.n_samples,
            centers=self.n_clusters,
            cluster_std=3.0,
            random_state=GLOBAL_RANDOM_STATE)
        self.kmeans = SKKMeans(
            n_clusters=self.n_clusters,
            init='random',
            n_init=1,
            max_iter=1,
            algorithm='lloyd',
            random_state=GLOBAL_RANDOM_STATE)

        self.cluster_colors = [CLUSTER_PALETTE[i % len(CLUSTER_PALETTE)]
                               for i in range(self.n_clusters)]

    def _make_legend(self, ax, labels):
        patches = [
            mpatches.Patch(facecolor=self.cluster_colors[i],
                           edgecolor=BITROOT_PALETTE['text'],
                           linewidth=0.5,
                           label=labels['cluster_label'].format(n=i + 1))
            for i in range(self.n_clusters)
        ]
        patches.append(
            mpatches.Patch(facecolor='none', edgecolor='none', label=''))
        patches.append(
            plt.Line2D([0], [0], marker='X', color=BITROOT_PALETTE['text'],
                       markerfacecolor=BITROOT_PALETTE['white'],
                       markeredgecolor=BITROOT_PALETTE['text'],
                       markersize=10, markeredgewidth=2, label=labels['centroid_label']))
        return ax.legend(handles=patches, title=labels['legend_title'], frameon=False,
                         fontsize=8, title_fontsize=9,
                         loc='upper right', ncol=2)

    def main(self):
        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()
            ax.set_xlim(-20, 20)
            ax.set_ylim(-20, 20)

            self.scatter = ax.scatter(self.X[:, 0], self.X[:, 1], s=30,
                                      c='grey', edgecolor=BITROOT_PALETTE['text'],
                                      linewidth=0.4)
            self.centers = ax.scatter([], [], s=200, marker='X',
                                      facecolor=BITROOT_PALETTE['white'],
                                      edgecolor=BITROOT_PALETTE['text'],
                                      linewidth=2)

            ax.set_title(labels['title'],
                         fontsize=16, color=BITROOT_PALETTE['text'], pad=10)
            ax.set_xlabel(labels['xlabel'],
                          fontsize=14, color=BITROOT_PALETTE['text'])
            ax.set_ylabel(labels['ylabel'],
                          fontsize=14, color=BITROOT_PALETTE['text'])

            self.legend = self._make_legend(ax, labels)
            self.apply_style(ax)

            ani = FuncAnimation(fig, self.update, frames=30,
                                init_func=self.init_func, interval=10,
                                repeat=False)
            anim_path = self.config.resolve_output("animation", n_clusters=self.n_clusters, suffix=suffix)
            ani.save(output_path(anim_path), writer='pillow')

            static_path = self.config.resolve_output("static", n_clusters=self.n_clusters, suffix=suffix)
            fig.savefig(output_path(static_path), bbox_inches='tight', pad_inches=0.1)
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
    for k in KMeans().config.params["n_clusters"]:
        KMeans(n_clusters=k).main()

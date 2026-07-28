"""
Visualises the Traveling Salesman Problem across multiple city counts to
illustrate how brute-force complexity (n! routes) grows.  A separate plot
is generated for each value of ``n_cities`` in the JSON config.

If the number of cities exceeds the internal brute force limit, no
ideal route will be calculated. You can still use the example to illustrate
how much our problem has grown with more cities.

Figures
-------
- ``traveling_salesman_small_{n_cities}_cities.png`` / ``_NL.png`` — optimal-route plot (n ≤ 7)
- ``traveling_salesman_large_{n_cities}_cities.png`` / ``_NL.png`` — full-graph plot (n > 7)

Configuration
-------------
``CCPlots/plot_configs/traveling_salesman.json``
"""
import itertools
import math
import random

import matplotlib.pyplot as plt
import networkx as nx

from CCPlots.PlotExample import PlotExample
from CCPlots.config import output_path

# Increase this value at your own risk lol
_BRUTE_FORCE_LIMIT = 7


class TravelingSalesman(PlotExample):

    CONFIG_KEY = "traveling_salesman"

    @staticmethod
    def _generate_random_graph(n_cities):
        G = nx.complete_graph(n_cities)
        for (u, v) in G.edges():
            G.edges[u, v]['weight'] = random.randint(1, 100)
        return G

    @staticmethod
    def _solve_tsp_brute_force(G):
        nodes = list(G.nodes)
        min_path = None
        min_cost = float('inf')
        for path in itertools.permutations(nodes):
            cost = sum(G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
            cost += G[path[-1]][path[0]]['weight']
            if cost < min_cost:
                min_cost = cost
                min_path = path
        return min_path, min_cost

    def _plot_tsp_small(self, G, path, total_routes, cost, labels, suffix):
        pos = nx.spring_layout(G, seed=42)
        fig, ax = self.create_figure()

        nx.draw(G, pos, with_labels=True, node_color=self.resolve_color('node_color'),
                node_size=500, ax=ax)

        tsp_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)] + [(path[-1], path[0])]
        nx.draw_networkx_edges(G, pos, edgelist=tsp_edges, width=2,
                               edge_color=self.resolve_color('optimal_edge'), ax=ax)

        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, ax=ax)

        ax.set_title(
            labels["title_small"].format(n_cities=G.number_of_nodes(),
                                         total_routes=total_routes),
            color=self.text_color)
        ax.axis('off')

        fname = self.config.resolve_output("small", n_cities=G.number_of_nodes(),
                                           suffix=suffix)
        fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)

    def _plot_tsp_large(self, G, total_routes, labels, suffix):
        pos = nx.spring_layout(G, seed=42)
        fig, ax = self.create_figure()

        nx.draw(G, pos, with_labels=True, node_color=self.resolve_color('node_color'),
                node_size=500, ax=ax)

        ax.set_title(
            labels["title_large"].format(n_cities=G.number_of_nodes(),
                                         total_routes=total_routes),
            color=self.text_color)
        ax.axis('off')

        self.save_figure(fig, "large", n_cities=G.number_of_nodes(), suffix=suffix)

    def main(self):
        n_cities_list = self.config.run["n_cities"]
        random.seed(42)

        for _locale, labels, suffix in self.iter_locales():
            for n in n_cities_list:
                G = self._generate_random_graph(n)
                total_routes = math.factorial(n)

                if n <= _BRUTE_FORCE_LIMIT:
                    path, cost = self._solve_tsp_brute_force(G)
                    self._plot_tsp_small(G, path, total_routes, cost, labels, suffix)
                else:
                    self._plot_tsp_large(G, total_routes, labels, suffix)

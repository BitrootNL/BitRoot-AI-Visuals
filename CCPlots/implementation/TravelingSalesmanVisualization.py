"""
Visualises the Traveling Salesman Problem on a small complete graph
(currently restricted to 2 and 4 cities). The brute-force optimal route is
highlighted. Edge weights are displayed on every connection.

Figures
-------
- ``tsp_small_{n_cities}_cities.png`` / ``_NL.png`` — optimal-route plot (n ≤ 20)
- ``tsp_large_{n_cities}_cities.png`` / ``_NL.png`` — full-graph plot (n > 20)

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
from CCPlots.config import BITROOT_PALETTE, load_example_config, output_path


class TravelingSalesman(PlotExample):

    CONFIG_KEY = "traveling_salesman"

    def __init__(self, n_cities=10):
        self.n_cities = n_cities
        self.G = self._generate_random_graph()

    def _generate_random_graph(self):
        G = nx.complete_graph(self.n_cities)

        for (u, v) in G.edges():
            G.edges[u, v]['weight'] = random.randint(1, 100)

        return G

    def _solve_tsp_brute_force(self):
        nodes = list(self.G.nodes)
        min_path = None
        min_cost = float('inf')

        for path in itertools.permutations(nodes):
            cost = sum(self.G[path[i]][path[i + 1]]['weight'] for i in range(len(path) - 1))
            cost += self.G[path[-1]][path[0]]['weight']

            if cost < min_cost:
                min_cost = cost
                min_path = path

        return min_path, min_cost

    def _plot_tsp_solution(self, path, filename, total_routes, cost, labels):
        pos = nx.spring_layout(self.G, seed=42)

        fig, ax = self.create_figure()

        nx.draw(self.G, pos, with_labels=True, node_color=BITROOT_PALETTE['primary'],
                node_size=500, ax=ax)

        tsp_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)] + [(path[-1], path[0])]
        nx.draw_networkx_edges(self.G, pos, edgelist=tsp_edges, width=2,
                               edge_color=BITROOT_PALETTE['success'], ax=ax)

        edge_labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, pos, edge_labels=edge_labels, ax=ax)

        ax.set_title(
            labels["title_small"].format(n_cities=self.n_cities, total_routes=total_routes),
            color=BITROOT_PALETTE['text'])
        ax.axis('off')

        fig.savefig(output_path(filename), bbox_inches='tight', pad_inches=0.1)
        plt.close(fig)

    def main(self):
        total_routes = math.factorial(self.n_cities)

        for _locale, labels, suffix in self.iter_locales():

            if self.n_cities <= 20:
                path, cost = self._solve_tsp_brute_force()
                print(f"Optimal path: {path}")
                print(f"Total cost: {cost}")
                print(f"Total possible routes: {total_routes:,}")

                fname = self.config.resolve_output("small", n_cities=self.n_cities, suffix=suffix)
                self._plot_tsp_solution(
                    path, output_path(fname), total_routes, cost, labels)
            else:
                pos = nx.spring_layout(self.G, seed=42)

                fig, ax = self.create_figure()
                nx.draw(self.G, pos, with_labels=True, node_color=BITROOT_PALETTE['tertiary'],
                        node_size=500, ax=ax)
                ax.set_title(
                    labels["title_large"].format(n_cities=self.n_cities, total_routes=total_routes),
                    color=BITROOT_PALETTE['text'])
                ax.axis('off')

                self.save_figure(fig, "large", n_cities=self.n_cities, suffix=suffix)


if __name__ == "__main__":
    cfg = load_example_config("traveling_salesman")
    for n in cfg.run["n_cities"]:
        TravelingSalesman(n_cities=n).main()

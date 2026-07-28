"""
NetworkX drawing of a feed-forward neural network with configurable layer
sizes (default 3 -> 5 -> 5 -> 2). Input nodes are primary, hidden nodes
tertiary, output nodes secondary.

Figures
-------
- ``nn_schematic.png`` / ``_NL.png`` — node-and-edge network schematic

Configuration
-------------
``CCPlots/plot_configs/neural_net_schematic.json``
"""
import networkx as nx

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE


class NeuralNetSchematic(PlotExample):

    CONFIG_KEY = "neural_net_schematic"

    def __init__(self, n_input_nodes=3, hidden_layers: tuple[int] = (5, 5), n_output_nodes=2):
        self.layers = [n_input_nodes] + list(hidden_layers) + [n_output_nodes]

    def main(self):
        G: nx.Graph = nx.Graph()
        positions = {}
        neuron_index = 0

        layer_count = len(self.layers)

        x_spacing = 6 / (layer_count - 1)
        y_spacing = 1.2

        colors = [
            BITROOT_PALETTE['primary'],
            *([BITROOT_PALETTE['tertiary']] * (layer_count - 2)),
            BITROOT_PALETTE['secondary']
        ]

        for layer_index, num_neurons in enumerate(self.layers):
            for neuron in range(num_neurons):
                x = layer_index * x_spacing
                y = -neuron * y_spacing + (num_neurons - 1) * y_spacing / 2

                positions[neuron_index] = (x, y)
                G.add_node(neuron_index, layer=layer_index)

                if layer_index > 0:
                    prev_layer_start = sum(self.layers[:layer_index - 1]) if layer_index > 1 else 0
                    prev_layer_end = prev_layer_start + self.layers[layer_index - 1]
                    for prev_neuron in range(prev_layer_start, prev_layer_end):
                        G.add_edge(prev_neuron, neuron_index)

                neuron_index += 1

        for _locale, labels, suffix in self.iter_locales():
            fig, ax = self.create_figure()

            nx.draw_networkx_edges(G, pos=positions, edge_color="gray", width=1.5, ax=ax)

            neuron_index = 0
            for layer_index, num_neurons in enumerate(self.layers):
                nodes = list(range(neuron_index, neuron_index + num_neurons))
                nx.draw_networkx_nodes(G, pos=positions, nodelist=nodes, node_size=600,
                                       node_color=colors[layer_index], ax=ax)
                neuron_index += num_neurons

            for layer_index, num_neurons in enumerate(self.layers):
                x = layer_index * x_spacing
                if layer_index == 0:
                    label = labels["input"]
                elif layer_index == layer_count - 1:
                    label = labels["output"]
                else:
                    label = f"{labels['hidden']} {layer_index}"
                y_bottom = min(y for (xx, y) in positions.values())
                ax.text(x, y_bottom - 0.75, label, ha='center', fontsize=12,
                        fontweight='bold', color=BITROOT_PALETTE['text'])

            ax.set_title(labels["title"], fontsize=14, color=BITROOT_PALETTE['text'])
            self.apply_style(ax)
            ax.axis('off')

            self.save_figure(fig, "default", suffix=suffix)

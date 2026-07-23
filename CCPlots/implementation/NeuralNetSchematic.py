import matplotlib.pyplot as plt
import networkx as nx

from CCPlots.PlotExample import PlotExample
from CCPlots.config import BITROOT_PALETTE, apply_bitroot_style, output_path


TEXT_BY_LOCALE = {
    "en": {
        "title": "Neural Network Schematic",
        "input": "Input",
        "output": "Output",
        "hidden": "Hidden",
    },
    "nl": {
        "title": "Neuraal netwerkschema",
        "input": "Invoer",
        "output": "Uitvoer",
        "hidden": "Verborgen",
    },
}


class NeuralNetSchematic(PlotExample):

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

        for locale, labels in (("en", TEXT_BY_LOCALE["en"]), ("nl", TEXT_BY_LOCALE["nl"])):
            fname = f"nn_schematic{'_NL' if locale == 'nl' else ''}.png"

            fig, ax = plt.subplots(figsize=(12, 6), facecolor=BITROOT_PALETTE['background'])
            ax.set_facecolor(BITROOT_PALETTE['background'])

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
            apply_bitroot_style(ax)
            ax.axis('off')

            fig.savefig(output_path(fname), bbox_inches='tight', pad_inches=0.1)
            plt.close(fig)

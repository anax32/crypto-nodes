import sys
from os.path import join

'''
In this script we try to compare the result of graph drawing
with different layouts with plotly visualization library
Here we use a predefined graph saved as pickle format
you can use any other graph as input to the function
'''

import networkx as nx
from plotly_visualize import visualize_graph

def get_edge_weights(G):
    try:
      G[0][0]["weight"]
      return [G[u][v]['weight'] for u, v in G.edges()]
    except KeyError:
      return [1 for _, _ in G.edges()]


def get_node_sizes(G):
    node_sizes = nx.get_node_attributes(G, 'importance').values()
    return node_sizes


def get_node_labels(G):
    return G.nodes()


if __name__ == "__main__":
    input_graph = sys.argv[1]
    output_dir = sys.argv[2]

    graph = nx.read_gpickle(input_graph)
    node_sizes = None #get_node_sizes(graph)
    edge_weights = None #get_edge_weights(graph)
    node_labels = None #get_node_labels(graph)
    layout = "spectral"
    visualize_graph(graph,
                    node_labels,
                    node_sizes,
                    edge_weights,
                    layout,
                    filename=join(output_dir, layout+".html"),
                    title=layout)
    #visualize_graph(graph, node_labels, node_sizes, layout, filename="outputs/"+layout+".html", title="")



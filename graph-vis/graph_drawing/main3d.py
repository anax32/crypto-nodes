import sys
import logging

from os.path import join

from plotly_visualize import visualize_graph_3d
import networkx as nx

from main import (get_edge_weights,
                  get_node_sizes)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def get_node_labels(G):
    return G.nodes()


graph_file = sys.argv[1]
output_dir = sys.argv[2]

logger.info("reading from '%s'" % graph_file)
logger.info("writing to '%s'" % output_dir)

G = nx.read_gpickle(graph_file)
node_sizes = None #get_node_sizes(graph)
edge_weights = None #get_edge_weights(graph)
node_labels = None #get_node_labels(graph)

logger.info("read graph with N=%i, E=%i" % (G.number_of_nodes(), G.number_of_edges()))

layout = "graphviz"
filename= join(output_dir, layout+"3d.html")

logger.info("drawing graph to '%s'" % filename)
visualize_graph_3d(G, node_labels, node_sizes, filename=filename, title="3D visualization")

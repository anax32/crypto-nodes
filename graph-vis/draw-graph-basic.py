"""
basic example of reading items from the db
"""
import os
import sys
import logging

from os.path import basename

from mongodb_reader import from_mongodb
from text_reader import from_text

import networkx as nx

# setup the log
logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# load the graph
graph_file = sys.argv[1]
logger.info("reading graph from '%s'" % graph_file)
G = nx.read_gpickle(graph_file)

logger.info("number of nodes: %i" % G.number_of_nodes())
logger.info("number of edges: %i" % G.number_of_edges())

# draw the graph with matplotlib
import matplotlib.pyplot as plt
plt.figure(figsize=(15,15))

logger.info("computing layout...")
# https://networkx.github.io/documentation/stable/reference/generated/networkx.drawing.nx_agraph.graphviz_layout.html
pos = nx.spring_layout(G)
#pos = nx.planar_layout(G)

# https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.drawing.nx_pylab.draw_networkx.html?highlight=node_size
nx.draw(G, pos=pos, node_size=1, alpha=0.5)
output_filename="/output-images/graph.png"
logger.debug("saving to '%s'" % output_filename)
plt.savefig(output_filename, dpi=100)

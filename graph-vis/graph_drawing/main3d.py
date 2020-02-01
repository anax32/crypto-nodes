import sys
import logging

from os.path import join, exists
from random import choice

import numpy as np

from plotly_visualize import visualize_graph_3d
import networkx as nx

from main import (get_edge_weights,
                  get_node_sizes)

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
logger.addHandler(handler)

# get the graph file
graph_file = sys.argv[1]
output_dir = sys.argv[2]

logger.info("reading graph from '%s'" % graph_file)
logger.info("writing to '%s'" % output_dir)

# read the file
G = nx.read_gpickle(graph_file)
node_sizes = None #get_node_sizes(graph)
edge_weights = None #get_edge_weights(graph)
node_labels = None #get_node_labels(graph)

logger.info("read graph with N=%i, E=%i" % (G.number_of_nodes(), G.number_of_edges()))

# get a subgraph
if False:
  # get a random sub-graph
  nodes = list(G.nodes())
  R_nodes = [choice(nodes) for _ in range(5000)]
  S = G.subgraph(R_nodes)
elif False:
  # get subgraph by degree
#  keep_nodes = [node for node, degree in G.degree().items() if degree > 1] # good long
  keep_nodes = [node for node, degree in G.degree().items() if degree > 2]
  S = G.subgraph(keep_nodes)
elif True:
  # get connected component graphs
  nodes = [c for c in sorted(nx.connected_components(G),
                             key=len, reverse=True) if len(c) > 80]

  node_idx = {}

  for i, n in enumerate(nodes):
    print("%4i: %i" % (i, len(n)))
    node_idx.update ({n_idx: i for n_idx in n})

  # get the subgraph of all nodes in connected components
  S = G.subgraph([a for n in nodes for a in n])

  rnd_min = -1
  rnd_max = 1

  initial_pos = {node: (float(node_idx[node]*10) + np.random.uniform(low=rnd_min, high=rnd_max),
                        0.0 + np.random.uniform(low=rnd_min, high=rnd_max))
                       for node in S.nodes()}
else:
  assert False

logger.info("cropped graph to N=%i, E=%i" % (S.number_of_nodes(), S.number_of_edges()))

# if node
positions = nx.get_node_attributes(S, "pos")

if len(positions) != len(S.nodes()):
  logger.info("got %i positions, recreating..." % len(positions))

  # FIXME: use graph-tool:sfdp_layout
  positions = nx.spring_layout(S, dim=2, pos=initial_pos, k=0.5, iterations=200)
  logger.info("computed node positions")

  positions_xyz = {n: (positions[n][0], positions[n][1], S.degree(n))
                   for n in positions}

  nx.set_node_attributes(S, "pos", positions_xyz)

# create the html output
layout = "graphviz"
filename= join(output_dir, layout+"3d.html")

logger.info("drawing graph to '%s'" % filename)
visualize_graph_3d(S,
                   node_labels,
                   node_sizes,
                   filename=filename, title="3D visualization")

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


# get the generators based on the storage environment
if sys.argv[1] == "mongodb":
  transaction_edge_fn = from_mongodb
elif sys.argv[1] == "text":
  transaction_edge_fn = from_text

# create a graph
G = nx.Graph()

# get all transactions from the generator
# FIXME: wrap this in tqdm, we need the total count?
for txid, input_txid in transaction_edge_fn():
  G.add_node(txid)
  G.add_node(input_txid)
  G.add_edge(txid, input_txid)

# output some graph stats
logger.info("number of nodes: %i" % G.number_of_nodes())
logger.info("number of edges: %i" % G.number_of_edges())

# save the graph pickle
pkl_file = "%s.pkl" % basename(os.environ["GRAPH_FILE"])
logger.info("writing to '%s'" % pkl_file)
nx.write_gpickle(G, pkl_file)

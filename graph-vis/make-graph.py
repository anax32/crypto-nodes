"""
basic example of reading items from the db
"""
import os
import sys
import logging

from pymongo import MongoClient
from pprint import pprint

import networkx as nx

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# build the uri for the connection
uri = "mongodb://%s:%s@%s:%i" % (os.environ["MONGODB_USER"],
                                 os.environ["MONGODB_PASS"],
                                 os.environ["MONGODB_HOST"],
                                 int(os.environ["MONGODB_PORT"]))

db_name = os.environ["MONGODB_DATABASE"]
cl_name = os.environ["MONGODB_COLLECTION"]
node_count = int(os.environ["NODE_COUNT"])

logger.info("using: '%s'" % uri)
logger.info("processing %i nodes in %s:%s" % (node_count, db_name, cl_name))

# connect
client = MongoClient(uri)
db = client[db_name]
txs = db[cl_name]

# get some stuff
logger.info("estimated document count: %i" % txs.estimated_document_count())

# query non-coinbase transactions
query={"vin.coinbase": {"$exists": False}}
proj={"txid": 1,
      "vin.txid": 1}
# alt. to include address information
proj_w_addr={"txid": 1,
             "vin.txid": 1,
             "vin.vout": 1,
             "vout.scriptPubKey.addresses": 1}

# create a graph
G = nx.Graph()

# add txs to graph
for record in txs.find(query, proj).limit(node_count):
  pprint(record)
  G.add_node(record["txid"])

  for intx in record["vin"]:
    G.add_node(intx["txid"])

    G.add_edge(record["txid"], intx["txid"])

print("number of nodes: %i" % G.number_of_nodes())
print("number of edges: %i" % G.number_of_edges())


# draw the graph
import matplotlib.pyplot as plt

logger.info("computing layout...")
# https://networkx.github.io/documentation/stable/reference/generated/networkx.drawing.nx_agraph.graphviz_layout.html
pos = nx.spring_layout(G)
#pos = nx.planar_layout(G)

logger.info("drawing...")
nx.draw(G, pos=pos, node_size=1)

logger.info("saving graph image")
plt.savefig("/output-images/graph.png", dpi=800)

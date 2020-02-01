"""
basic example of reading items from the db
"""
import os
import logging

from pymongo import MongoClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def from_mongodb():
  """read transaction data from a mongodb database
  database connection settings are set in environment variables
  json object format is expected to be the same as
  the output of decoderawtransaction rpc in bitcoind
  """
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
  proj={"txid": 1, "vin.txid": 1}
  # alt. to include address information
  proj_w_addr={"txid": 1,
               "vin.txid": 1,
               "vin.vout": 1,
               "vout.scriptPubKey.addresses": 1}

  # add txs to graph
  if node_count is None or node_count < 1:
    node_count = txs.estimated_document_count()

  for record in txs.find(query, proj).limit(node_count):
    for in_tx in record["vin"]:
      yield record["txid"], in_tx["txid"]

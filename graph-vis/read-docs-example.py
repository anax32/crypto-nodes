"""
basic example of reading items from the db
"""
import os
import sys
import logging

from pymongo import MongoClient
from pprint import pprint

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

logger.info("using: '%s'" % uri)

db_name = os.environ["MONGODB_DATABASE"]
cl_name = os.environ["MONGODB_COLLECTION"]

# connect
client = MongoClient(uri)
db = client[db_name]
txs = db[cl_name]

# get some stuff
logger.info("estimated document count: %i" % txs.estimated_document_count())

for record in txs.find().limit(10):
  pprint(record)


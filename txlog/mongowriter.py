"""
Simple class for writing dicts to a mongodb
"""
import logging

from pymongo import MongoClient

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class MongoWriter(object):
  """write transactions to a mongodb
     after translating with bitcoind rpc
  """
  def __init__(self, host, port,
                     user, password,
                     authSource="admin",
                     database="default-database",
                     collection="default-collection"):
    """
    setup the connection to the mongodb
    clear the authentication
    get the database and collections
    """
    logger.info("writing transactions to mongodb:'%s:%i'" % (host, port))
    self.mdb_client = MongoClient(host=host,
                                  port=port,
                                  username=user,
                                  password=password,
                                  authSource=authSource)
    self.db = self.mdb_client[database]
    self.col = self.db[collection]
    logger.info("using mongodb db: '%s', collection: '%s'" % (database, collection))

  def __call__(self, data):
    """
    add the dict to the collection
    """
    logger.debug("mdb inserting keys: %s" % ", ".join(data.keys()))
    self.col.insert_one(data)

  def __del__(self):
    """
    close the connection to the remote db
    """
    logger.info("closing mongodb connection")
    self.mdb_client.close()

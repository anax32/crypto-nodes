import logging
from time import perf_counter as clock


logger = logging.getLogger(__name__)


def getblockinfo(block_height, rpc):
  """get data about a block at a particular height in the chain
  """
  T = clock()

  try:
    block_hash = rpc("getblockhash", [block_height]).json()["result"]
  except KeyError:
    logger.error("key error in block hash")
    return

  try:
    block_data = rpc("getblock", [block_hash, True]).json()["result"]
  except KeyError:
    logger.error("key error in block data")
    return

  logger.info("getblockinfo in %0.2fs", (clock()-T))

  return block_data

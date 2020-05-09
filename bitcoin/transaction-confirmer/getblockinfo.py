import requests
import json
import os
import logging
import sys
import itertools
from time import perf_counter as clock
import gzip

from bitcoinrpc import create_rpc_callback

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info(__name__)


def getblockinfo(block_height, rpc_callback):
  """get data about a block at a particular height in the chain
  """
  T = clock()

  try:
    block_hash = rpc_callback("", "getblockhash", [block_height]).json()["result"]
  except KeyError:
    logger.error("key error in block hash")
    return

  try:
    block_data = rpc_callback("", "getblock", [block_hash, True]).json()["result"]
  except KeyError:
    logger.error("key error in block data")
    return

  return block_data

if __name__ == "__main__":
  TX_BLOCK_SIZE = int(os.environ["TX_READ_COUNT"])
  iter = 0

  rpc_callback = create_rpc_callback()

  stop_iters = False

  fields = ["hash", "time", "difficulty", "nTx", "weight", "chainwork"]

  print(" ".join(fields))

  # read a file of transaction ids
  for iter in range(int(sys.argv[1]), int(sys.argv[2])):
    logger.debug("block %i" % iter)

    blockinfo = getblockinfo(iter, rpc_callback)
    print(" ".join([str(blockinfo[k]) for k in fields]))

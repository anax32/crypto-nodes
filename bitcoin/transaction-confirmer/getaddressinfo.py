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


def getaddressinfo(addresses, rpc_callback):
  """pass a list of txids in to get a list of confimration counts
  """
  err = (-1, -1, "-1") # error marker

  methods = ["getaddressinfo", "validateaddress"]
  fieldmap = [(("ischange", "ischange"),), (("isvalid", "isvalid"),)]
  infos = {}

  T = clock()

  for address in addresses:
    for method, fields in zip(methods, fieldmap):
      response = rpc_callback("", method, [address])

      if response.status_code == 500:
        logger.debug("%i 500 response" % address)
        break

      # process the transaction
      try:
        data = response.json()
      except Exception as e:
        logger.exception("could not parse json response")
        continue

      for field in fields:
        try:
          infos[address].update({field[0]: data["result"][field[1]]})
        except KeyError:
          infos[address] = {field[0]: data["result"][field[1]]}

  logger.info("%i %s in %0.2fs (%i)" %
                 (len(addresses), method, clock()-T, len(infos)))

  return infos

if __name__ == "__main__":
  TX_BLOCK_SIZE = int(os.environ["TX_READ_COUNT"])
  iter = 0

  rpc_callback = create_rpc_callback()

  if sys.argv[1].endswith(".gz"):
    open_fn = gzip.open
  else:
    open_fn = open

  stop_iters = False

  # read a file of transaction ids
  with open_fn(sys.argv[1], "rb") as f:
    # read a file of transaction ids
    for iter in itertools.count():
      logger.debug("block %i (%i tx)" % (iter, iter*TX_BLOCK_SIZE))
      try:
        txs = [next(f).decode("utf-8").strip() for _ in range(TX_BLOCK_SIZE)]
      except StopIteration:
        stop_iters = True

      infos = getaddressinfo(txs, rpc_callback)

      for addr, info in infos.items():
        print("%s %s %s" % (addr, info["ischange"], info["isvalid"]))

      if stop_iters is True:
        break

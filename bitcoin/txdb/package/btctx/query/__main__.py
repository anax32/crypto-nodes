import os
import logging
import sys
import json
import argparse
import gzip

import btctx


logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_rpc():
  # get the RPC object
  rpc = btctx.rpc.bitcoind.BitcoinRPC(
      os.environ["BITCOIND_RPC_USER"],
      os.environ["BITCOIND_RPC_PASSWORD"],
      os.getenv("BITCOIND_HOST", "localhost"),
      int(os.getenv("BITCOIND_PORT", 8332))
  )

  # check the availablity of the rpc server
  network_info = rpc("getnetworkinfo")
  logger.debug("network_info response: '%s'", str(network_info))

  blockchain_info = rpc("getblockchaininfo")
  logger.debug("blockchain_info: '%s'", str(blockchain_info))

  return rpc


if __name__ == "__main__":
  rpc = get_rpc()

  # read transactions from a file
  fname = sys.argv[1]
  logger.debug("reading from '%s'", fname)

  print("input,output")

  with gzip.open(fname, "r") as f:
    for tx_t in f:
      tx = json.loads(tx_t)
      logger.debug("read '%s'", tx["txid"])

      s = {
          "inputs": btctx.query.transaction.get_input_addresses(tx, rpc),
          "outputs": btctx.query.transaction.get_output_addresses(tx, rpc)
      }

      # make a list of input/output pairs
      for t in [",".join((i, o)) for o in s["inputs"] for i in s["outputs"]]:
        print(t)

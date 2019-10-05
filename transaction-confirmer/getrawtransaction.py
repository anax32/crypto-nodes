import requests
import json
import os
import logging
import sys
import itertools
from time import clock
import gzip

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info(__name__)

def getrawtransaction(txids, session=None):
  """pass a list of txids in to get a list of confimration counts
  """
  url = "http://%s:%s" % (os.environ["RPC_HOST"], os.environ["RPC_PORT"])
  err = (-1, -1, "-1") # error marker

  if session is None:
    session = requests.Session()

  session.headers.update({"content-type": "text/plain",
                          "cache-control": "no-cache"})
  session.auth=(os.environ["RPC_USER"], os.environ["RPC_PASS"])

  logger.info("sending %i transactions to '%s'" % (len(txids), url))
  confirmations = []

  T = clock()

  for txid in txids:
    response = session.post(
      url,
      data=json.dumps({
        "jsonrpc": "2.0",
        "method": "getrawtransaction",
        "params": [txid, True],
        "id": "get_confirmation_count"
      }))

    if response.status_code == 500:
      # 500 indicates the tid was not found, which may be good for
      # marking as unconfirmed, but we never know for sure if a tid
      # will never be confirmed, only that at this current point, it
      # has not been confirmed. So we treat all "not found" the same
      # way, which is -1 for confirmations
      # sort of expect a not found to be 404
      err = response.json()
      logger.error("rpc.status_code: %i (%s)" % (response.status_code,
                                                 response.text))
      confirmations.append((-1, -1, err["error"]["code"]))
    elif response.status_code != 200:
      logger.error("rpc.status_code: %i (%s)" % (response.status_code,
                                                 response.text))
      confirmations.append(err)
    else:
      try:
        txc = response.json()
        confirmations.append((txc["result"]["confirmations"],
                              txc["result"]["blockhash"],
                              "found"))
      except Exception as e:
        logger.exception("could not parse json response")
        confirmations.append(err)

  logger.info("got %i confirmations in %0.2fs" % (len(confirmations), clock()-T))
  return confirmations

if __name__ == "__main__":
  TX_BLOCK_SIZE = int(os.environ["TX_READ_COUNT"])
  iter = 0

  session = requests.Session()

  if sys.argv[1].endswith(".gz"):
    open_fn = gzip.open
  else:
    open_fn = open

  # read a file of transaction ids
  with open_fn(sys.argv[1], "rb") as f:
    for iter in itertools.count():
      logger.info("block %i (%i tx)" % (iter, iter*TX_BLOCK_SIZE))
      try:
        txs = [next(f).decode("utf-8").strip() for _ in range(TX_BLOCK_SIZE)]
      except StopIteration:
        logger.exception("end of file")
        break

      confirmations = getrawtransaction(txs, session=session)

      with open_fn(sys.argv[2], "ab") as r:
        for txid, confirmation in zip(txs, confirmations):
          output = "%s %s %s\n" % (txid, confirmation[0], confirmation[1])
          r.write(output.encode())

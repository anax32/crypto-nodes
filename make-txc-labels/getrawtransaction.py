import requests
import json
import os
import logging
import sys

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.info(__name__)

def getrawtransaction(txids):
  """pass a list of txids in to get a list of confimration counts
  """
  url = "http://%s:%s" % (os.environ["RPC_HOST"], os.environ["RPC_PORT"])
  logger.info(url)
  headers = {"content-type": "text/plain",
             "cache-control": "no-cache"}

  logger.info("got %i transactions" % len(txids))
  confirmations = []

  for txid in txids:
    logger.info("url: '%s'" % url)
    response = requests.post(
      url,
      data=json.dumps({
        "jsonrpc": "2.0",
        "method": "getrawtransaction",
        "params": [txid, True],
        "id": "get_confirmation_count"
      }),
      headers=headers,
      auth=(os.environ["RPC_USER"], os.environ["RPC_PASS"]))

    logger.info(response.status_code)

    conf = (-1, -1)
    try:
      txc = response.json()
      conf = (txc["result"]["confirmations"],
              txc["result"]["blockhash"])
    except Exception as e:
      logger.exception("could not parse json response")

    confirmations += conf

  logger.info("got %i confirmations" % len(confirmations))
  return confirmations

if __name__ == "__main__":
  # read a file of transaction ids
  with open(sys.argv[1], "r"), open(sys.argv[2]) as f, r:
    txid = f.readline()
    conf = get_raw_transaction([txid])
    print("%s %s %s" % (txid, conf[0][0], conf[0][1]), file=r)

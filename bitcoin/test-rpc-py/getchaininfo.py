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

logger.info("getchaininfo.py")

for k in os.environ:
  logger.debug("env: %s: %s" % (k, os.environ[k]))

def main():
    url = "http://%s:%s" % (os.environ["RPC_HOST"], os.environ["RPC_PORT"])
    logger.info(url)
    headers = {"content-type": "text/plain",
               "cache-control": "no-cache"}

    # Example echo method
    payloads = [{
        "jsonrpc": "2.0",
        "method": "getnetworkinfo",
        "params": [],
    },
    {
        "jsonrpc": "2.0",
        "method": "getblockchaininfo",
        "params": [],
    }]

    for payload in payloads:
      logger.info("url: '%s'" % url)
      response = requests.post(
          url,
          data=json.dumps(payload),
          headers=headers,
          auth=(os.environ["RPC_USER"], os.environ["RPC_PASS"]))

      logger.info(response.status_code)
      logger.info(response.text)

if __name__ == "__main__":
    main()

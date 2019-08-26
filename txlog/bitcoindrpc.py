import logging
import json

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class BitcoinRPC(object):
  """bitcoind rpc message passer
     https://upcoder.com/7/bitcoin-rpc-from-python
  """
  def __init__(self, user, password, host="localhost", port=18332):
    self.session = requests.Session()
    self.url = "http://%s:%i" % (host, port)
    self.headers = {"content-type": "application/json"}
    self.user = user
    self.password = password

  def __call__(self, method, *params):
    payload = json.dumps({"method": method,
                          "params": list(params),
                          "jsonrpc": "2.0"})
    logger.debug("sending rpc: '%s'" % payload)
    resp = self.session.post(self.url,
                             headers=self.headers,
                             data=payload,
                             auth=(self.user, self.password))
    logger.debug("rpc returned: %i (%s)" % (resp.status_code, resp.text))
    if resp.status_code == 200:
      return resp.json()["result"]
    else:
      logger.error("%i: %s" % (resp.status_code, resp.text))

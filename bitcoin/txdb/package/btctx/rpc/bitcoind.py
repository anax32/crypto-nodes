"""Simple wrapper to send json rpc calls to the bitcoind endpoint

NB: this defaults to the 18332 port (bitcoind default is 8332)
"""
import logging
import requests


logger = logging.getLogger(__name__)


class BitcoinRPC(object):
  """bitcoind rpc message passer

     TODO: multiple host endpoints
     TODO: exception handling for bad connections
  """
  def __init__(self, user, password, host="localhost", port=18332):
    self.session = requests.Session()
    self.url = "http://%s:%i" % (host, port)
    self.headers = {"content-type": "application/json", "cache-control": "no-cache"}
    self.session.auth = (user, password)

  def __call__(self, method, *params):
    payload = {"method": method,
               "params": list(params),
               "jsonrpc": "2.0"}

    try:
      resp = self.session.post(self.url,
                               headers=self.headers,
                               json=payload)
    except Exception as e:
      logger.exception(e)
      return None

    logger.debug("rpc returned: %i (%s...)" % (resp.status_code, resp.text[:20]))
    if resp.status_code == 200:
      return resp.json()["result"]
    else:
      logger.error("%i: %s" % (resp.status_code, resp.text))
      return {}

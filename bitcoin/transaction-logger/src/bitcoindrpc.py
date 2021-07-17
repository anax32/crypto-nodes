"""Simple wrapper to send json rpc calls to the bitcoind endpoint

NB: this defaults to the 18332 port (bitcoind default is 8332)
"""
import logging
import json

import requests


logger = logging.getLogger(__name__)


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
    try:
      resp = self.session.post(self.url,
                               headers=self.headers,
                               json=payload,
                               auth=(self.user, self.password))
    except Exception as e:
      logger.exception(e)

    logger.debug("rpc returned: %i (%s)" % (resp.status_code, resp.text))
    if resp.status_code == 200:
      return resp.json()["result"]
    else:
      logger.error("%i: %s" % (resp.status_code, resp.text))

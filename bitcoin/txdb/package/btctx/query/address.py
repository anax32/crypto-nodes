"""address related analytics"""

import logging


logger = logging.getLogger(__name__)


def getaddressinfo(address, rpc):
  """pass a list of addresses to get ischange or isvalid attributes from the node
  """
  err = (-1, -1, "-1") # error marker

  addrinfo_keys = set(["isscript", "iswitness", "ischange"])
  validateaddr_keys = set(["isvalid"])

  info = {
      **{k:v for k,v in rpc("getaddressinfo", [address]).items() if k in addrinfo_keys},
      **{k:v for k,v in rpc("validateaddress", [address]).items() if k in validateaddr_keys}
  }

  return info

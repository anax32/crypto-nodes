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

handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_output_value(tx):
  """ sum the outputs of a transaction
  """
  try:
    return sum([x["value"] for x in tx["vout"]])
  except KeyError:
    return 0


def get_input_value(tx, rpc_callback):
  """sum the input value of a transaction
     by get the output keys of all the inputs
  """
  inputs = []

  for tx_in in tx["vin"]:
    try:
      tx_x = rpc_callback("", "getrawtransaction", [tx_in["txid"], True]).json()["result"]
    except (KeyError, ValueError):
      continue

    for tx_x_out in tx_x["vout"]:
      if tx_x_out["n"] == tx_in["vout"]:
        inputs.append(tx_x_out["value"])

  return sum([x for x in inputs])


def get_transaction_info(txids, rpc_callback, fields, field_defaults, field_fns):
  """yield transaction info for a bunch of transaction ids
     txids: list or generator of transaction ids
     rpc_callback: rpc callback object
     fields: names of fields to get from the response
     field_defaults: default values for the fields
     field_fns: functions to extract the field values from the response
  """
  for txid in txids:
    # setup the default response
    tx = {k: field_defaults[k] for k in fields}

    # do the rpc call
    response = rpc_callback("", "getrawtransaction", [txid, True])

    if response.status_code != 200:
      # 500 indicates the tid was not found, which may be good for
      # marking as unconfirmed, but we never know for sure if a tid
      # will never be confirmed, only that at this current point, it
      # has not been confirmed. So we treat all "not found" the same
      # way, which is -1 for confirmations
      # sort of expect a not found to be 404
      logger.debug("rpc.status_code: %i (%s)" % (response.status_code,
                                                 response.text))
    else:
      try:
        # get the transaction data
        tx_data = response.json()["result"]
        # parse the transaction
        for field in fields:
          try:
            tx[field] = field_fns[field](tx_data)
          except (KeyError, ValueError):
            logger.error("could not parse field: '%s'" % field)

      except KeyError:
        logger.error("could not parse response: '%s'" % response.text)

    # return the transaction info
    yield tx


if __name__ == "__main__":
  fields = ["txid",
            "confirmation-count",
            "confirmed",
            "block",
            "size",
            "output-value",
            "input-value",
            "fee",
            "change"]

  field_defaults = {"txid": "0",
                    "confirmation-count": 0,
                    "confirmed": False,
                    "block": "0",
                    "size": 0,
                    "output-value": 0,
                    "input-value": 0,
                    "fee": 0,
                    "change": 0
                   }

  field_fns = {"txid": lambda tx_data: tx_data["txid"],
               "confirmation-count": lambda tx_data: int(tx_data["confirmations"]),
               "confirmed": lambda tx_data: int(tx_data["confirmations"]) > 0,
               "block": lambda tx_data: tx_data["blockhash"],
               "size": lambda tx_data: tx_data["size"],
               "output-value": get_output_value,
               "input-value": lambda tx_data: get_input_value(tx_data, rpc_callback),
               "fee": lambda x: 0,
               "change": lambda x: 0
              }

  def line_parser(f):
    for x in f:
      yield x.decode("utf-8").strip()

  rpc_callback = create_rpc_callback()

  if sys.argv[1].endswith(".gz"):
    open_fn = gzip.open
  else:
    open_fn = open

  # read a file of transaction ids
  with open_fn(sys.argv[1], "rb") as f:
    # print a header
    print(" ".join(fields))

    # print the body
    for tx_info in get_transaction_info(line_parser(f),
                                        rpc_callback,
                                        fields,
                                        field_defaults,
                                        field_fns):
      print(" ".join([str(tx_info[field]) for field in fields]))

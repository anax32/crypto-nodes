import logging


logger = logging.getLogger(__name__)


def get_output_value(tx):
  """ sum the outputs of a transaction
  """
  try:
    return sum([x["value"] for x in tx["vout"]])
  except KeyError:
    return 0


def get_input_value(tx, rpc):
  """sum the input value of a transaction
     by get the output keys of all the inputs
  """
  inputs = []

  for tx_in in tx["vin"]:
    try:
      tx_x = rpc("getrawtransaction", [tx_in["txid"], True])
    except (KeyError, ValueError):
      continue

    for tx_x_out in tx_x["vout"]:
      if tx_x_out["n"] == tx_in["vout"]:
        inputs.append(tx_x_out["value"])

  return sum([x for x in inputs])


def gettransactioninfo(txid, rpc, field_set=None, field_defaults=None, field_fns=None):
  """yield transaction info for a bunch of transaction ids

     txids: list or generator of transaction ids
     rpc_callback: rpc callback object
     fields: names of fields to get from the response
     field_defaults: default values for the fields
     field_fns: functions to extract the field values from the response
  """
  if field_set is None:
    field_set = (["txid", "confirmation-count", "confirmed",
                  "block", "size", "output-value",
                  "input-value", "fee", "change"])

  if field_defaults is None:
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

  if field_fns is None:
    field_fns = {"txid": lambda x: x["txid"],
                 "confirmation-count": lambda x: int(x["confirmations"]),
                 "confirmed": lambda x: int(x["confirmations"]) > 0,
                 "block": lambda x: x["blockhash"],
                 "size": lambda x: x["size"],
                 "output-value": get_output_value,
                 "input-value": lambda x: get_input_value(x),
                 "fee": lambda x: 0,
                 "change": lambda x: 0
                }

  # setup the default response
  tx = {k: field_defaults[k] for k in fields}

  # get the transaction data
  tx_data = rpc("getrawtransaction", [txid, True])

  # parse the transaction
  for field in fields:
    try:
      tx[field] = field_fns[field](tx_data)
    except (KeyError, ValueError):
      logger.error("could not parse field: '%s'", field)

  return tx


def get_input_addresses(tx, rpc):
  """get list of input addresses to a transaction

     for this we have to do an rpc call to getrawtransaction to get the tx details
  """
  # get the input transactions
  addr = [x for vin in tx["vin"] for v in rpc("getrawtransaction", vin["txid"])["vout"]
            if v["n"] == vin["vout"]
              for x in v["scriptPubKey"]["addresses"]
         ]
  return set(addr)


def get_output_addresses(tx, rpc):
  """get list of output addresses to a transaction"""
  addr = []

  for v in tx["vout"]:
    addr += set(v["scriptPubKey"]["addresses"])

  return set(addr)


def transaction_matrix(txs, rpc):
  """get a sparse transaction matrix
  """
  smat = {}
  for tx in txs:
    smat[tx["txid"]] = {
        "inputs": get_input_addresses(tx, rpc),
        "outputs": get_output_addresses(tx, rpc)
    }
  return smat

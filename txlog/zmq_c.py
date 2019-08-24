# Copyright (c) 2014-2016 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import binascii
import zmq
import os
import itertools
import logging
import sys
import gzip
import json

import requests
from pymongo import MongoClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


"""
required environment variables
"""
assert "RAWTX_SOURCE_ADDR" in os.environ
assert "OUTPUT_FILE" in os.environ or "MONGODB_HOST" in os.environ

if "MONGODB_HOST" in os.environ:
  assert "MONGODB_PORT" in os.environ
  assert "BITCOIND_RPC_USER" in os.environ
  assert "BITCOIND_RPC_PASSWORD" in os.environ
  assert "BITCOIND_HOST" in os.environ
  assert "BITCOIND_PORT" in os.environ



class BitcoinRPC(object):
  """bitcoind rpc message passer
     https://upcoder.com/7/bitcoin-rpc-from-python
  """
  def __init__(self, user, password, host="localhost", port=18332):
    self.session = requests.Session()
    self.url = "http://%s:%s@%s:%i" % (user, password, host, port)
    self.headers = {"content-type": "application/json"}

  def __call__(self, method, *params):
    payload = json.dumps({"method": method,
                          "params": list(params),
                          "jsonrpc": "2.0"})
    resp = self.session.get(self.url,
                            headers=self.headers,
                            data=payload)
    if resp.status_code == 200:
      return resp.json()
    else:
      logger.error("%i: %s" % (resp.status_code, resp.text))


class MongoWriter(object):
  """write transactions to a mongodb
     after translating with bitcoind rpc
  """
  def __init__(self, host, port):
    logger.info("writing transactions to '%s:%i'" % (host, port))
    self.mdb_client = MongoClient(host, port)
    self.btc_db = self.mdb_client["btc"]
    self.tx_cols = self.btc_db["transactions"]
    self.bitcoind_rpc = BitcoinRPC(os.environ["BITCOIND_RPC_USER"],
                                   os.environ["BITCOIND_RPC_PASSWORD"],
                                   os.environ["BITCOIND_HOST"],
                                   int(os.environ["BITCOIND_PORT"]))

  def __call__(self, hex_string):
    logger.info("decoding transaction")
    logger.info(hex_string)
    logger.info(hex_string.hex())
    tx_json = self.bitcoind_rpc("decoderawtransaction", hex_string.hex())
    logger.info("tx.keys: %s" % ", ".join(tx_json.keys()))
    self.tx_cols.insert_one(tx_json)

  def __del__(self):
    self.mdb_client.close()


def make_transaction_filename(count):
  """consistent filename for transaction logs
  """
  max_count = int(os.environ["RAWTX_COUNT_PER_FILE"])
  return "%s_%08i.log" % (os.environ["OUTPUT_FILE"], count/max_count)

def rotate_transaction_file(count):
  """return true if we should create a new transaction file
  """
  return (count+1) % int(os.environ["RAWTX_COUNT_PER_FILE"]) == 0

def create_transaction_file_handle(count):
  if "RAWTX_COMPRESSED_LOGS" in os.environ:
    f = gzip.open("%s.gz" % make_transaction_filename(count), "wb")
  else:
    f = open(make_transaction_filename(count), "wb")

  logger.info("created transaction file: '%s'" % f.name)
  return f


class TextWriter(object):
  """write transactions to a text file
  """
  def __init__(self, fname, compressed=False):
    if compressed:
      logger.info("writing compressed transactions to: '%s'" % fname)
    else:
      logger.info("writing transactions to: '%s'" % fname)

    self.tx_file = create_transaction_file_handle(0)

  def __call__(self, hex_string):
    self.tx_file.write(binascii.hexlify(body) + b"\n")

    if rotate_transaction_file(tx_idx) is True:
      logger.info("swapping transaction file (%i transactions)" % tx_idx)
      logger.info("closing transaction file: '%s'" % tx_file.name)
      self.tx_file.close()

      self.tx_file = create_transaction_file_handle(tx_idx)

  def __del__(self):
    logger.info("closing final file handle")
    self.tx_file.close()


def get_transaction_writer():
  """create a writer function depedning on the env vars
  """
  if "MONGODB_HOST" in os.environ:
    return MongoWriter(host=os.environ["MONGODB_HOST"],
                       port=int(os.environ["MONGODB_PORT"]))
  elif "OUTPUT_FILE" in os.environ:
    return TextWriter(fname=os.environ["OUTPUT_FILE"],
                      compressed="RAWTX_COMPRESSED_LOGS" in os.environ)
  else:
    logger.warning("No transaction writer created")
    return None



"""
zmq stuff
"""
context = zmq.Context()

socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"rawtx")
socket.connect(os.environ["RAWTX_SOURCE_ADDR"])

logger.info("reading from '%s'" % os.environ["RAWTX_SOURCE_ADDR"])
logger.info("output filename pattern: '%s'" % os.environ["OUTPUT_FILE"])

writer = get_transaction_writer()

try:
  for tx_idx in itertools.count():
    logger.debug("waiting on idx %i" % tx_idx)
    msg = socket.recv_multipart()
    logger.debug("got body (len: %i (%i, %i))" % (len(msg), len(msg[0]), len(msg[1])))
    body = msg[1]

    if writer is not None:
      writer(body)

except KeyboardInterrupt:
  logger.info("cleanup")
  context.destroy()
except Exception as e:
  logger.exception(e)
  context.destroy()

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
assert "OUTPUT_FILE" in os.environ
assert "RAWTX_COUNT_PER_FILE" in os.environ

if "RAWTX_COMPRESSED_LOGS" in os.environ:
  logger.info("writing compressed logs with gzip")


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

"""
zmq stuff
"""
context = zmq.Context()

socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"rawtx")
socket.connect(os.environ["RAWTX_SOURCE_ADDR"])

logger.info("reading from '%s'" % os.environ["RAWTX_SOURCE_ADDR"])
logger.info("output filename pattern: '%s'" % os.environ["OUTPUT_FILE"])

try:
  tx_file = create_transaction_file_handle(0)

  for tx_idx in itertools.count():
    logger.debug("waiting on idx %i" % tx_idx)
    msg = socket.recv_multipart()
    logger.debug("got body (len: %i (%i, %i))" % (len(msg), len(msg[0]), len(msg[1])))
    body = msg[1]
    tx_file.write(binascii.hexlify(body) + b"\n")

    if rotate_transaction_file(tx_idx) is True:
      logger.info("swapping transaction file (%i transactions)" % tx_idx)
      logger.info("closing transaction file: '%s'" % tx_file.name)
      tx_file.close()

      tx_file = create_transaction_file_handle(tx_idx)

except KeyboardInterrupt:
  logger.info("cleanup")
  context.destroy()
except Exception as e:
  logger.exception(e)
  context.destroy()

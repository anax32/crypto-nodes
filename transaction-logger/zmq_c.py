import zmq
import os
import itertools
import logging
import sys

from textwriter import TextWriter
from mongowriter import MongoWriter
from bitcoindrpc import BitcoinRPC
from s3_uploader import upload_file_to_s3

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

def upload_on_write_complete(filename):
  logger.info("upload_on_write_complete('%s')" % filename)

  # upload the file to s3
  upload_file_to_s3(os.environ["AWS_BUCKET_NAME"],
                    os.environ["AWS_TX_PREFIX"],
                    filename)

  # delete the original file to save disk
  logger.info("removing file '%s' after upload" % filename)
  os.remove(filename)
  logger.info("upload complete")

def get_transaction_writer():
  """create a writer function depedning on the env vars
  """
  rpc = BitcoinRPC(os.environ["BITCOIND_RPC_USER"],
                   os.environ["BITCOIND_RPC_PASSWORD"],
                   os.environ["BITCOIND_HOST"],
                   int(os.environ["BITCOIND_PORT"]))

  if "MONGODB_HOST" in os.environ:
    mdb = MongoWriter(host=os.environ["MONGODB_HOST"],
                      port=int(os.environ["MONGODB_PORT"]),
                      user=os.environ["MONGODB_USER"],
                      password=os.environ["MONGODB_PASSWORD"],
                      database=os.environ["MONGODB_DATABASE"],
                      collection=os.environ["MONGODB_COLLECTION"])
    def unpack_and_write_mdb(hex_string):
      logger.debug("decoding: '%s'" % hex_string.hex())

      try:
        decoded_hex_string = rpc("decoderawtransaction", hex_string.hex())
      except Exception as e:
        logger.exception(e)

      if decoded_hex_string is not None:
        mdb(decoded_hex_string)
      else:
        logger.warning("rpc call returned None (skipping record)")

    return unpack_and_write_mdb


  elif "OUTPUT_FILE" in os.environ:
    import json

    txw = TextWriter(max_count=int(os.environ["RAWTX_COUNT_PER_FILE"]),
                     fname=os.environ["OUTPUT_FILE"],
                     compressed="RAWTX_COMPRESSED_LOGS" in os.environ,
                     write_complete_fn=upload_on_write_complete)

    def unpack_and_write_txt(hex_string):
      logger.debug("decoding: '%s'" % hex_string.hex())
      try:
        decoded_hex_string = rpc("decoderawtransaction", hex_string.hex())
      except Exception as e:
        logger.exception(e)

      if decoded_hex_string is not None:
        txw(json.dumps(decoded_hex_string))
      else:
        logger.warning("rpc call returned None (skipping record)")

    return unpack_and_write_txt

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

logger.info("recving from '%s'" % os.environ["RAWTX_SOURCE_ADDR"])

writer = get_transaction_writer()
logger.info("using tx writer: '%s'" % str(writer))

try:
  for tx_idx in itertools.count():
    logger.debug("waiting on idx %i" % tx_idx)
    msg = socket.recv_multipart()
    logger.debug("got body (len: %i (%i, %i))" % (len(msg), len(msg[0]), len(msg[1])))
    body = msg[1]

    if writer is not None:
      writer(body)
    else:
      logger.debug("writer is None, not logging tx")

except KeyboardInterrupt:
  logger.info("cleanup")
  context.destroy()
except Exception as e:
  logger.exception(e)
  context.destroy()

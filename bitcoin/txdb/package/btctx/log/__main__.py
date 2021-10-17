import zmq
import os
import itertools
import logging
import sys
import json
import time

from btctx.persist.text import TextWriter
from btctx.persist.mongow import MongoWriter
from btctx.persist.s3 import upload_file_to_s3
from btctx.rpc.bitcoind import BitcoinRPC

logger = logging.getLogger()
logger.setLevel(os.getenv("LOG_LEVEL", "INFO"))

handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter("%(asctime)s:%(name)s:%(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


logging.getLogger("botocore").setLevel(logging.WARNING)


"""
required environment variables
"""
assert "RAWTX_SOURCE_ADDR" in os.environ

if "MONGO_LOGGER" in os.environ and int(os.environ["MONGO_LOGGER"]) != 0:
  assert "MONGODB_HOST" in os.environ
  assert "MONGODB_PORT" in os.environ
  assert "BITCOIND_RPC_USER" in os.environ
  assert "BITCOIND_RPC_PASSWORD" in os.environ
  assert "BITCOIND_HOST" in os.environ
  assert "BITCOIND_PORT" in os.environ

if "FILE_LOGGER" in os.environ and int(os.environ["FILE_LOGGER"]) != 0:
  assert "RAWTX_COUNT_PER_FILE" in os.environ
  assert "FILENAME_STUB" in os.environ


def get_transaction_writers():
  """create writer functions depedning on the env vars
  """
  writers = []

  if "MONGO_LOGGER" in os.environ and int(os.environ["MONGO_LOGGER"]) != 0:
    mdb = MongoWriter(host=os.environ["MONGODB_HOST"],
                      port=int(os.environ["MONGODB_PORT"]),
                      user=os.environ["MONGODB_USER"],
                      password=os.environ["MONGODB_PASSWORD"],
                      database=os.environ["MONGODB_DATABASE"],
                      collection=os.environ["MONGODB_COLLECTION"])
    def unpack_and_write_mdb(decoded_hex_string):
      mdb(decoded_hex_string)

    writers.append(unpack_and_write_mdb)

  if "FILE_LOGGER" in os.environ and int(os.environ["FILE_LOGGER"]) != 0:
    write_complete_fn = None

    if "AWS_BUCKET_NAME" in os.environ and len(os.environ["AWS_BUCKET_NAME"]) > 0:
      logger.info("s3 upload to '%s/%s", os.environ["AWS_BUCKET_NAME"], os.environ["AWS_FILE_PREFIX"])
      write_complete_fn=lambda fileobj, filename: upload_file_to_s3(os.environ["AWS_BUCKET_NAME"],
                                                           os.environ["AWS_FILE_PREFIX"],
                                                           fileobj,
                                                           filename,
                                                           extra_args={"ContentType": "application/gzip"})

    txw = TextWriter(max_count=int(os.getenv("RAWTX_COUNT_PER_FILE", 20000)),
                     fname_stub=os.environ["FILENAME_STUB"],
                     write_complete_fn=write_complete_fn)

    def unpack_and_write_txt(decoded_hex_string):
      txw(json.dumps(decoded_hex_string))

    writers.append(unpack_and_write_txt)

  if "STDOUT_LOGGER" in os.environ and int(os.environ["STDOUT_LOGGER"]) != 0:
    def unpack_and_write_stdout(decoded_hex_string):
      print(json.dumps(decoded_hex_string))

    writers.append(unpack_and_write_stdout)

  if len(writers) < 1:
    logger.warning("No transaction writers created")

  return writers


def get_node_info():
  """return information about the node running the process
  """
  import time
  import datetime

  return {
      "time": str(datetime.datetime.now().replace(microsecond=0).isoformat()),
      "tz": ",".join([str(x) for x in time.tzname])
  }


if __name__ == "__main__":
  """
  zmq stuff
  """
  # set up the sockets
  context = zmq.Context()

  socket = context.socket(zmq.SUB)
  socket.setsockopt(zmq.SUBSCRIBE, b"rawtx")
  socket.connect(os.environ["RAWTX_SOURCE_ADDR"])

  logger.info("recving from '%s'" % os.environ["RAWTX_SOURCE_ADDR"])

  # get the RPC object
  rpc = BitcoinRPC(os.environ["BITCOIND_RPC_USER"],
                   os.environ["BITCOIND_RPC_PASSWORD"],
                   os.environ["BITCOIND_HOST"],
                   int(os.environ["BITCOIND_PORT"]))

  # check the availablity of the rpc server
  network_info = rpc("getnetworkinfo")
  logger.info("network_info response: '%s'", str(network_info))

  blockchain_info = rpc("getblockchaininfo")
  logger.info("blockchain_info: '%s'", str(blockchain_info))

  # get the topic handlers
  topic_handlers = {
    b"rawtx": lambda x: rpc("decoderawtransaction", x)
  }

  # get the embelishments
  data_embelishments = {
    "node-info": lambda x: get_node_info(),
    "zmq-topic": lambda x: x.decode()
  }

  # get the writers
  writers = get_transaction_writers()
  logger.info("using tx writers: '%s'" % str(writers))

  # endless loop
  try:
    while True:
      topic, body, sequence = socket.recv_multipart()
      logger.debug("[%s] %i bytes", topic.decode(), len(body))

      # decode the data using the handlers
      try:
        log_data = topic_handlers[topic](body.hex())
      except Exception as e:
        logger.exception(e)
        continue

      if log_data is None:
        logger.warning("rpc call returned None (skipping record)")
        continue

      # embelishments
      try:
        log_data.update({"extra": {name: fn(topic) for name, fn in data_embelishments.items()}})
      except Exception as e:
        logger.exception(e)
        continue

      # pass the decoded json on to the writers
      if len(writers) > 0:
        for writer in writers:
          writer(log_data)
      else:
        logger.warning("no writers in use, not logging")

  except KeyboardInterrupt:
    logger.info("exiting for KeyboardInterrupt")

    # shutdown the writers
    for writer in writers:
      del writer

    context.destroy()
  except Exception as e:
    logger.exception(e)
    context.destroy()

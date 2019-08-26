import os
import logging
import gzip


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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
    logger.info("initial logfile created at: '%s'" % self.tx_file.name)

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

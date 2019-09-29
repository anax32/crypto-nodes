import os
import logging
import gzip
import binascii
from multiprocessing import Process


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def make_transaction_filename(count, max_count, fname_stub):
  """consistent filename for transaction logs
  """
  idx = count/max_count
  logger.info("transaction batch: %i" % idx)
  return "%s_%08i.log" % (fname_stub, idx)

def rotate_transaction_file(count, max_count):
  """return true if we should create a new transaction file
  """
  return count % max_count == 0

def create_transaction_file_handle(count, max_count, fname_stub):
  filename = make_transaction_filename(count, max_count, fname_stub)
  logger.info("writing to '%s'" % filename)

  if "RAWTX_COMPRESSED_LOGS" in os.environ:
    f = gzip.open("%s.gz" % filename, "wb")
  else:
    f = open(filename, "wb")

  logger.info("created transaction file: '%s'" % f.name)
  return f


class TextWriter(object):
  """write transactions to a text file
  """
  def __init__(self, max_count, fname, compressed=False, write_complete_fn=None):
    if compressed:
      logger.info("writing compressed transactions to: '%s'" % fname)
    else:
      logger.info("writing transactions to: '%s'" % fname)

    self.tx_idx = 0
    self.fname_stub = fname
    self.max_count = max_count

    self.tx_file = create_transaction_file_handle(self.tx_idx, self.max_count, self.fname_stub)
    assert self.tx_file is not None

    self.write_complete_fn = write_complete_fn

    logger.info("initial logfile created at: '%s'" % self.tx_file.name)

  def __call__(self, tx_string):
    self.tx_file.write((tx_string + "\n").encode())
    self.tx_idx += 1
    logger.debug("logging transaction %i" % self.tx_idx)

    if rotate_transaction_file(self.tx_idx, self.max_count) is True:
      logger.info("swapping transaction file (%i transactions)" % self.tx_idx)
      logger.info("closing transaction file: '%s'" % self.tx_file.name)
      self.tx_file.flush()
      last_filename = self.tx_file.name
      self.tx_file.close()

      if self.write_complete_fn is not None:
        # run the callback in another process
        p = Process(target=self.write_complete_fn, args=(last_filename,))
        p.start()

      # create a new file to write on
      self.tx_file = create_transaction_file_handle(self.tx_idx, self.max_count, self.fname_stub)

  def __del__(self):
    logger.info("closing final file handle after %i transactions" % self.tx_idx)
    self.tx_file.flush()
    self.tx_file.close()

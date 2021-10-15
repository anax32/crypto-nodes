"""writes transaction data to a compressed text file in memory

when `max_count` transactions have been collect, the `write_complete_fn` is called
with the filename and file handle as arguments
"""
import logging

import io
import gzip
import json

from multiprocessing import Process

logger = logging.getLogger(__name__)


class TextWriter(object):
  """write transactions to an in-memory compressed text file

     txw = TextWriter(200, "txns", lambda f, filename: open(filename, w).write(f.read()))
  """
  def __init__(self, max_count, fname_stub, write_complete_fn=None):
    self.fname_stub = fname_stub
    self.max_tx_count = max_count
    self.tx_buf = None
    self.tx_file = None
    self.tx_count = 0

    self.write_complete_fn = write_complete_fn

  def should_rotate_transaction_file(self):
    """return true if we should create a new transaction file
    """
    return self.__len__() % self.max_tx_count == 0

  def __len__(self):
    return self.tx_count

  def execute_callbacks(self, txid=None):
    if self.tx_file is None:
      return

    logger.info("swapping %i txs buffer", self.__len__())

    filename = "%s_%s.log.gz" % (self.fname_stub, txid or str(self.__len__()/self.max_tx_count))
    self.tx_file.close()
    self.tx_buf.seek(0)

    if self.write_complete_fn is not None:
      # run the callback in another process
      p = Process(target=self.write_complete_fn, args=(self.tx_buf, filename,))
      p.start()

  def rotate_transaction_file(self, txid):
    # notify listerners we've finished this file
    self.execute_callbacks(txid)

    # create a new file buffer
    self.tx_buf = io.BytesIO()
    self.tx_file = gzip.GzipFile(fileobj=self.tx_buf, mode="wb")

    # reset the transaction count
    self.tx_count = 0

  def __call__(self, tx):
    """process a transaction dict by adding it to a file, creating a new file if necessary"""
    txid = json.loads(tx)["txid"]

    if self.tx_file is None or self.should_rotate_transaction_file():
      self.rotate_transaction_file(txid)

    # write to the log
    self.tx_file.write((tx + "\n").encode())
    self.tx_count += 1

    if self.__len__() % (self.max_tx_count/10) == 0:
      logger.info("tx %i/%i", self.__len__()%self.max_tx_count, self.max_tx_count)
    else:
      logger.debug("tx %i", self.__len__())


  def __del__(self):
    logger.info("final close after %i transactions", self.__len__())
    self.tx_file.flush()
    self.tx_file.close()

# Copyright (c) 2014-2016 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import binascii
import zmq
import os

assert "RAWTX_SOURCE_ADDR" in os.environ

context = zmq.Context()

socket = context.socket(zmq.SUB)
socket.setsockopt(zmq.SUBSCRIBE, b"rawtx")
socket.connect(os.environ["RAWTX_SOURCE_ADDR"])

try:
  while True:
    msg = socket.recv_multipart()
    body = msg[1]
    print (binascii.hexlify(body))

except KeyboardInterrupt:
    context.destroy()

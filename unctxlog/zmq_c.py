# Copyright (c) 2014-2016 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import array
import binascii
import zmq
import struct

ip = "127.0.0.1"
#ip = "172.17.0.2"
port = 28332

print("A")
zmqContext = zmq.Context()

print("B %s" % str(zmqContext))
zmqSubSocket = zmqContext.socket(zmq.SUB)
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, b"hashblock")
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, b"hashtx")
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, b"rawblock")
zmqSubSocket.setsockopt(zmq.SUBSCRIBE, b"rawtx")

print("C %s" % str(zmqSubSocket))

zmqSubSocket.connect("tcp://%s:%i" % (ip, port))

print("D %s" % str(zmqSubSocket))

try:
    while True:
        msg = zmqSubSocket.recv_multipart()
#        msg = zmqSubSocket.recv()
#        print(msg)
        topic = str(msg[0])
        body = msg[1]

        print("topic: '%s', body: '%s'" % (str(topic), str(body)))
        sequence = "Unknown";
        if len(msg[-1]) == 4:
          msgSequence = struct.unpack('<I', msg[-1])[-1]
          sequence = str(msgSequence)
          print("unknown")
        if topic == b"hashblock":
            print ('- HASH BLOCK ('+sequence+') -')
            print (binascii.hexlify(body))
        elif topic == b"hashtx":
            print ('- HASH TX  ('+sequence+') -')
            print (binascii.hexlify(body))
        elif topic == b"rawblock":
            print ('- RAW BLOCK HEADER ('+sequence+') -')
            print (binascii.hexlify(body[:80]))
        elif topic == b"rawtx":
            print ('- RAW TX ('+sequence+') -')
            print (binascii.hexlify(body))

except KeyboardInterrupt:
    zmqContext.destroy()

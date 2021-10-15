#!/bin/bash


(cd bitcoind-from-src ;

docker build \
  --target fullnode \
  -t anax32/bitcoind:latest \
  -t anax32/bitcoind:v0.21.1 \
  .
)

(cd cortex ;

docker build \
  -t anax32/btc/cortex \
  .
)

docker build -t anax32/btc/logger .

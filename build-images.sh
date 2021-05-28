#!/bin/bash -u


#
# bitcoin
#
docker build -t anax32/crypto-nodes.bitcoin -f bitcoin/bitcoind-from-repo/Dockerfile ./bitcoin

#
# ethereum
#
docker build -t anax32/crypto-nodes.ethereum -f eth/node/Dockerfile ./eth/node
docker build -t anax32/crypto-nodes.ethereum:mine-latest -f eth/mine/Dockerfile ./eth/mine

#
# monero
#
docker build -t anax32/crypto-nodes.xmr:cpu-latest -f ./xmrig/Dockerfile.cpu  .

#
# monitoring
#
docker build -t anax32/nvidia-log -f nvidia/log/Dockerfile ./nvidia/log

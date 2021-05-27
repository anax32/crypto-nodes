#!/bin/bash -u

docker build -t anax32/crypto-nodes.bitcoin -f bitcoin/bitcoind-from-repo/Dockerfile ./bitcoin

docker build -t anax32/crypto-nodes.ethereum -f eth/node/Dockerfile ./eth/node
docker build -t anax32/crypto-nodes.ethereum-classic -f etc/node/Dockerfile ./etc/node

docker build -t anax32/crypto-nodes.ethereum:mine-latest -f eth/mine/Dockerfile ./eth/mine
docker build -t anax32/crypto-nodes.ethereum-classic:mine-latest -f etc/mine/Dockerfile ./etc/mine

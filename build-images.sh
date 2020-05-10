#!/bin/bash -u

docker build -t crypto-nodes.bitcoin -f bitcoin/bitcoind-from-repo/Dockerfile ./bitcoin

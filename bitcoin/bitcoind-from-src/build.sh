#!/bin/bash

#
# latest
#

# build env first and cache
# this image takes a long time to build and is ~2Gb
docker build \
  --target build-stage \
  --cache-from anax32/bitcoind:build-latest \
  --cache-from anax32/bitcoind:build-v0.20.1 \
  -t anax32/bitcoind:build-latest \
  -t anax32/bitcoind:build-v0.20.1 \
  --build-arg BITCOIN_VERSION_TAG=v0.20.1 \
  .

# fullnode compile using cache
# this image is the deployment and ~80Mb
docker build \
  --target fullnode \
  --cache-from anax32/bitcoind:build-latest \
  --cache-from anax32/bitcoind:build-v0.20.1 \
  --cache-from anax32/bitcoind:latest \
  --cache-from anax32/bitcoind:v0.20.1 \
  -t anax32/bitcoind:latest \
  -t anax32/bitcoind:v0.20.1 \
  .

#
# build a bunch of versions from github releases
#
for v in v0.20.0 v0.19.1 v0.19.0 v0.18.1 v0.18.0
do
  docker build \
    --target build-stage \
    --cache-from anax32/bitcoind:build-$v \
    -t anax32/bitcoind:build-v0.18.0 \
    --build-arg BITCOIN_VERSION_TAG=$v \
    .

  docker build \
    --target fullnode \
    --cache-from anax32/bitcoind:build-$v \
    --cache-from anax32/bitcoind:$v \
    -t anax32/bitcoind:$v \
    .
done

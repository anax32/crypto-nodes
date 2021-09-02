#!/bin/bash

docker build \
  -t anax32/btc-tx-log \
  .

RPCU=ed
RPCP=edpassword1

docker run \
  --rm \
  -e STDOUT_LOGGER=1 \
  -e RAWTX_SOURCE_ADDR="tcp://127.0.0.1:28832" \
  -e RAWTX_COUNT_PER_FILE=20000 \
  -e RAWTX_COMPRESSED_LOGS=1 \
  -e OUTPUT_FILE=/data/mempool \
  -e BITCOIND_RPC_USER=$RPCU \
  -e BITCOIND_RPC_PASSWORD=$RPCP \
  -e BITCOIND_HOST=127.0.0.1 \
  -e BITCOIND_PORT=8332 \
  -e LOG_LEVEL=WARNING \
  --network=host \
  -v $(pwd)/data:/data \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  anax32/btc-tx-log

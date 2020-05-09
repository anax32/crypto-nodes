#!/bin/bash

CONTAINER="bitcoindockerfile_bitcoind_1"
FILENAME=$1
echo "parsing: '$FILENAME'"

while read RAW_TRANSACTION
do
  sudo docker exec \
    $CONTAINER \
    bitcoin-cli \
      -conf=/config/bitcoin.conf \
      decoderawtransaction \
      $RAW_TRANSACTION
  break
done < $FILENAME

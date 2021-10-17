#!/bin/bash

##
#
# dogshit docker-compose networking ruins the RPC connectivity, so we do it all in network=host
#
##

cat << EOF > logger.env
FILE_LOGGER=1
RAWTX_SOURCE_ADDR=tcp://127.0.0.1:28832
RAWTX_COUNT_PER_FILE=200
BITCOIND_RPC_USER=ed
BITCOIND_RPC_PASSWORD=edpassword1
BITCOIND_HOST=127.0.0.1
BITCOIND_PORT=8332
AWS_BUCKET_NAME=transactions
AWS_FILE_PREFIX=txlog
AWS_S3_ENDPOINT=http://minioserver:9000
FILENAME_STUB=txn
MINIO_ROOT_USER=lolmybad
MINIO_ROOT_PASSWORD=lolmybadlol
MINIO_INITIAL_BUCKETS=transactions
LOG_LEVEL=DEBUG
AWS_ACCESS_KEY_ID=lolmybad
AWS_SECRET_ACCESS_KEY=lolmybadlol
EOF


# bitcoin core
docker run \
  -d \
  --rm \
  --env-file logger.env \
  --network=host \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  -u $(id -u):$(id -g) \
  -v /home/ed/data-disk/btc/data:/block-data \
  -v /home/ed/data-disk/btc/config:/config \
  --name btc-node \
  anax32/bitcoind

# minio storage
docker run \
  -d \
  --rm \
  --env-file logger.env \
  --network=host \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  -u $(id -u):$(id -g) \
  -v /home/ed/data-disk/btc/buckets:/data \
  --name storage \
  anax32/storage \
  /usr/bin/init-buckets.sh

storage_ip=127.0.0.1

# logger container
docker run \
  -it \
  --rm \
  --env-file logger.env \
  --network=host \
  -u $(id -u):$(id -g) \
  -v /home/ed/data-disk/btc/txdata:/data \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  --add-host minioserver:${storage_ip} \
  --name logger \
  anax32/btc/logger

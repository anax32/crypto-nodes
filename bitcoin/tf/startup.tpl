#!/bin/bash

apt-get update
apt-get install -y --no-install-recommends \
  awscli \
  docker.io

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws ecr get-login-password --region ${aws_region} | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.${aws_region}.amazonaws.com

# get the node container
docker pull ${node_repository}:${node_tag}
docker pull ${logger_repository}:${logger_tag}

mkdir /config

cat << EOF > /config/bitcoin.conf
rpcuser=${rpc_username}
rpcpassword=${rpc_password}
prune=550
zmqpubhashblock=tcp://127.0.0.1:28832
zmqpubhashtx=tcp://127.0.0.1:28832
zmqpubrawtx=tcp://127.0.0.1:28832
EOF

# run the node container
docker run \
  -d \
  --rm \
  --network=host \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  -v /data:/block-data \
  -v /config:/config \
  --name btc-node \
  ${node_repository}:${node_tag}

sleep 5

# setup the logging for the node container
docker exec \
  btc-node \
  bitcoin-cli \
    -rpcuser=${rpc_username} \
    -rpcpassword=${rpc_password} \
    logging "[\"all\"]" "[\"http\", \"bench\", \"tor\", \"qt\", \"leveldb\", \"net\", \"addrman\", \"selectcoins\", \"rand\", \"prune\", \"libevent\", \"walletdb\"]"

# run the log container
docker run \
  -d \
  --rm \
  -e FILE_LOGGER=1 \
  -e RAWTX_SOURCE_ADDR="tcp://127.0.0.1:28832" \
  -e RAWTX_COUNT_PER_FILE=${tx_count} \
  -e RAWTX_COMPRESSED_LOGS=1 \
  -e AWS_BUCKET_NAME=${aws_bucket_name} \
  -e AWS_FILE_PREFIX=${aws_prefix} \
  -e BITCOIND_RPC_USER=${rpc_username} \
  -e BITCOIND_RPC_PASSWORD=${rpc_password} \
  -e BITCOIND_HOST=127.0.0.1 \
  -e BITCOIND_PORT=8332 \
  -e LOG_LEVEL=DEBUG \
  --network=host \
  -v /tx-data:/data \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  --name btc-tx-logger \
  ${logger_repository}:${logger_tag}

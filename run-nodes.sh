
#!/bin/bash

#
# ethereum
#
docker run \
  -d \
  --name ethminer \
  --gpus all \
  -it \
  -e ETH_POOL_ADDR=eu1.ethermine.org \
  -e ETH_ADDR=0x2067000E3ca05c9007A556Ac4efe238805DB7400 \
  -e WORKER_NAME=work09 \
  --restart=always \
  --cpus="0.5" \
  anax32/crypto-nodes.ethereum:mine-latest

#docker run \
#  -d \
#  --name etcminer \
#  --gpus all \
#  -it \
#  -e ETH_POOL_ADDR=eu1-etc.ethermine.org \
#  -e ETH_ADDR=0x2067000E3ca05c9007A556Ac4efe238805DB7400 \
#  -e WORKER_NAME=work09 \
#  --restart=always \
#  --cpus="0.5" \
#  anax32/crypto-nodes.ethmine


#
# xmr
#
docker run \
  -d \
  --name xmrig \
  -e XMR_POOL_ADDR=pool.supportxmr.com:443 \
  -e XMR_ADDR=4AJin9Rwi4KE93rgyPKnds569UeXKgxdW7G9vvKUQCKrPYzHQMQmGrFezLq5GuX3Pfjo1wkiHu3jmGRUhRRufjYPBQPtKaH \
  -e WORKER_NAME=work01 \
  anax32/crypto-nodes.xmr:cpu-latest

docker run \
  -d \
  --name xmrig-solo \
  -e XMR_POOL_ADDR=gulf.moneroocean.stream:20128 \
  -e XMR_ADDR=4AJin9Rwi4KE93rgyPKnds569UeXKgxdW7G9vvKUQCKrPYzHQMQmGrFezLq5GuX3Pfjo1wkiHu3jmGRUhRRufjYPBQPtKaH \
  -e WORKER_NAME=work01 \
  anax32/crypto-nodes.xmr:cpu-latest

#
# monitoring
#
docker run \
  -d \
  --name gpu-monitor \
  --gpus all \
  -it \
  anax32/nvidia-log

# docker logs -f ethminer
# docker logs -f xmrig

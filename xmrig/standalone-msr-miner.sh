#!/bin/bash

docker stop xmrig-solo
docker rm xmrig-solo

docker run \
  -d \
  --name xmrig-solo \
  -e XMR_POOL_ADDR=gulf.moneroocean.stream:20128 \
  -e XMR_ADDR=4AJin9Rwi4KE93rgyPKnds569UeXKgxdW7G9vvKUQCKrPYzHQMQmGrFezLq5GuX3Pfjo1wkiHu3jmGRUhRRufjYPBQPtKaH \
  -e WORKER_NAME=work02 \
  --privileged \
  --cap-add ALL \
   -v /lib/modules:/lib/modules \
  anax32/crypto-nodes.xmr:cpu-latest

docker logs -f xmrig-solo

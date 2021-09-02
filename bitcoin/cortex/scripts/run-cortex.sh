#!/bin/bash

docker run \
  -it \
  --rm \
  --name cortex \
  --network=host \
  -e RPC_USERNAME=ed \
  -e RPC_PASSWORD=edpassword1 \
  anax32/cortex

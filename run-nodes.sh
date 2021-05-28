
#!/bin/bash

docker run \
  -d \
  --name ethminer \
  --gpus all \
  -it \
  -e ETH_WALLET=0x2067000E3ca05c9007A556Ac4efe238805DB7400 \
  --restart=always \
  --cpus="0.5" \
  crypto-nodes.ethmine

docker run \
  -d \
  --name xmrig \
  -v $(pwd)/xmrig/conf:/conf \
  crypto-nodes.xmr \
  /usr/bin/xmrig -c /conf/xmrig.cpu.conf

docker run \
  -d \
  --name gpu-monitor \
  --gpus all \
  -it \
  nvmon

# docker logs -f ethminer

docker logs -f ethminer

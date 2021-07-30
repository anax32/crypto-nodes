# Cortex blockchain explorer

Connects to a bitcoin node and offers an interface to the RPC functions of that node.

This allows a client side front end to browse the node data without exposing the RPC
credentials to the client and allows the possibility of using a different set of
credentials to access the frontend.

# usage

run a fullnode with the bitcoind daemon or a containerised version and set the config
to index transactions and expose the RPC service:

```bash
cat << EOF > $(pwd)/bitcoin.conf
server=1
rpcuser=${RPC_USERNAME}
rpcpassword=${RPC_PASSWORD}
txindex=1
EOF

docker run \
  -d \
  --rm \
  --network=host \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  -v $(pwd)/data:/block-data \
  -v $(pwd)/config:/config \
  --name btc-node \
  anax32/bitcoind
```

then run the cortex container:
```bash
docker build \
  -t anax32/cortex \
  .

docker run \
  -it \
  --rm \
  --network=host \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  -e RPC_USERNAME=${RPC_USERNAME} \
  -e RPC_PASSWORD=${RPC_PASSWORD} \
  -e API_PORT=8001 \
  anax32/cortex
```

and connect to: http://127.0.0.1:8001

read the swagger docs at: http://127.0.0.1:8001/docs

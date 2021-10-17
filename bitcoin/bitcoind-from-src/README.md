# Bitcoin Fullnode from source

Builds a docker image of the bitcoin core daemon from the github mirror:
https://github.com/bitcoin/bitcoin

Build contains:
+ wallet
+ zmq
+ transaction db

# Usage

Build docker image as a multi-stage build.
The first stage sets up the build environment,
second stage clones the repo and does the build,
third stage copies the binaries to a container with minium dependencies to run.

## Note on dependencies

`debian bullseye (11)` and `debian buster (10)` made different versions of `libevent*` and `libboost*` available
in package repositories: these variations are captured in the `build-args` `BOOST_VERSION` and `LIBEVENT_VERSION`
if  you wish the change the default debian base image.

## Build

Use this build script to cache the build environment:
```bash
docker build \
  -t anax32/bitcoind:latest \
  -t anax32/bitcoind:v22.0 \
  --build-arg BITCOIN_CORE_TAG=v22.0 \
  --build-arg BOOST_VERSION=1.74 \
  --build-arg LIBEVENT_VERSION=2.1-7 \
  bitcoind-from-src/
```

## Run

Run docker image by creating two directories `./data` and `./config` to store
block data and config outside the container.

```bash
docker run \
  -d \
  --rm \
  --network=host \
  --log-opt max-size=5m \
  --log-opt max-file=5 \
  --name btc-node \
  anax32/bitcoind
```

block chain data is stored in the container `/block-data` directory.

`bitcoin.conf` configuration script is loaded from the `/config/bitcoin.conf` container directory.

Default config held in the container is pulled from the [bitcoin github repo](https://raw.githubusercontent.com/bitcoin/bitcoin/master/share/examples/bitcoin.conf) in the `Dockerfile`.

### example hosted data and config

A local `bitcoin.conf` can be created and mounted over the `/config` directory to provide your own config.

```bash
mkdir -a data config

cat << EOF > config/bitcoin.conf
#rpc server
server=1
rpcuser=$RPC_USER
rpcpassword=$RPC_PASSWORD
rpcport=8332
# Maintain coinstats index used by the gettxoutsetinfo RPC (default: 0).
coinstatsindex=1
txindex=1
#zmqpubhashblock=tcp://127.0.0.1:28832
#zmqpubhashtx=tcp://127.0.0.1:28832
zmqpubrawtx=tcp://127.0.0.1:28832
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

# Disclaimer

You are responsible for your actions.

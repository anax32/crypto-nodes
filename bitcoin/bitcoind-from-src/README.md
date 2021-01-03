# Bitcoin Fullnode from source

Builds a docker image of the bitcoin core daemon from the github mirror:
https://github.com/bitcoin/bitcoin

Build contains:
+ wallet
+ zmq
+ transaction db

## Usage

Build docker image as a multi-stage build.
The first stage sets up the environment, clones the repo and does the build,
the second stage creates a containe with the binaries and minium dependencies to run.

Use this build script to cache the build environment:
```bash
# build env first and cache
# ~2Gb/~30 mins
docker build \
  --target build-stage \
  --cache-from anax32/bitcoind:build-latest \
  --cache-from anax32/bitcoind:build-v0.20.1 \
  -t anax32/bitcoind:build-latest \
  -t anax32/bitcoind:build-v0.20.1 \
  --build-arg BITCOIN_VERSION_TAG=v0.20.1 \
  .

# fullnode compile using cache
# ~120Mb/~1 min
docker build \
  --target fullnode \
  --cache-from anax32/bitcoind:build-latest \
  --cache-from anax32/bitcoind:build-v0.20.1 \
  --cache-from anax32/bitcoind:latest \
  --cache-from anax32/bitcoind:v0.20.1 \
  -t anax32/bitcoind:latest \
  -t anax32/bitcoind:v0.20.1 \
  .
```

Run docker image:
```bash
docker run \
  -u $(id -u):$(id -g) \
  -v $(pwd)/data:/block-data \
  anax32/bitcoind
```

block chain data is stored in the container `/block-data` dir
(in the above, this is the `$(pwd)/data` host mount).

`bitcoin.conf` configuration script is loaded from the `/config/bitcoin.conf` container directory.
Create a local `bitcoin.conf` and mount over this directory to provide your own config.
Default config is pulled from the [bitcoin github repo](https://raw.githubusercontent.com/bitcoin/bitcoin/master/share/examples/bitcoin.conf] at line 108 of the `Dockerfile`.

# Disclaimer

You are responsible for your actions.

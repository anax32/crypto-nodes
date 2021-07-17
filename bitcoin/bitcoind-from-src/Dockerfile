# github release tag
ARG BITCOIN_CORE_TAG=v0.18.0

# boost dev versions don't have the trailing .0, so we add
# the MINOR_VERSION via env subs
ARG BOOST_VERSION=1.67
ARG BOOST_DEV_SUFFIX=-dev
ARG BOOST_RELEASE_SUFFIX=.0

#
# build bitcoind from github.com source
#   ~2Gb, ~30 mins
#   see: https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md
#
FROM python:3 AS build-stage

ARG BITCOIN_CORE_TAG
ARG BOOST_VERSION
ARG BOOST_DEV_SUFFIX

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
              bsdmainutils \
              build-essential \
              libevent-dev \
              libboost-system$BOOST_VERSION$BOOST_DEV_SUFFIX \
              libboost-filesystem$BOOST_VERSION$BOOST_DEV_SUFFIX \
              libboost-test$BOOST_VERSION$BOOST_DEV_SUFFIX \
              libboost-thread$BOOST_VERSION$BOOST_DEV_SUFFIX

# zmq interface dependencies
RUN apt-get install -y --no-install-recommends \
              libzmq3-dev

# gui dependencies
RUN apt-get install -y --no-install-recommends \
              libqrencode-dev \
              libqt5core5a \
              libqt5dbus5 \
              libqt5gui5 \
              qttools5-dev \
              qttools5-dev-tools

# clone repo
ENV PROJECT_DIR=/btc/bitcoin
RUN mkdir /btc/

RUN git clone \
      --depth 1 \
      -b $BITCOIN_CORE_TAG \
      https://github.com/bitcoin/bitcoin.git $PROJECT_DIR

# build
WORKDIR $PROJECT_DIR

#
# configure the build environment with leveldb for a wallet
# see: https://github.com/bitcoin/bitcoin/blob/master/contrib/install_db4.sh
#
# build with low-mem for docker daemon
# see: https://github.com/bitcoin/bitcoin/blob/master/doc/build-unix.md#memory-requirements
RUN ./contrib/install_db4.sh $(pwd) && \
    export BDB_PREFIX="$(pwd)/db4" && \
    ./autogen.sh && \
    ./configure \
        BDB_LIBS="-L${BDB_PREFIX}/lib \-ldb_cxx-4.8" \
        BDB_CFLAGS="-I${BDB_PREFIX}/include" \
        CFLAGS="-O2" \
        CXXFLAGS="-O2 -I/usr/local/BerkeleyDB.4.8/include" \
        LDFLAGS="-L/usr/local/BerkeleyDB.4.8/lib"
##      --without-gui

RUN make && make install

# build the deployable image
# ~120Mb, ~1 min
FROM debian:buster-slim AS fullnode

ARG BITCOIN_CORE_TAG
ARG BOOST_VERSION
ARG BOOST_RELEASE_SUFFIX

# libzmq5 only need for zmq server
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
              libboost-system$BOOST_VERSION$BOOST_RELEASE_SUFFIX \
              libboost-filesystem$BOOST_VERSION$BOOST_RELEASE_SUFFIX \
              libboost-thread$BOOST_VERSION$BOOST_RELEASE_SUFFIX \
              libboost-chrono$BOOST_VERSION$BOOST_RELEASE_SUFFIX \
              libssl1.1 \
              libevent-pthreads-2.1-6 \
              libevent-2.1-6 \
              libzmq5 \
              sqlite3

COPY --from=build-stage /usr/local/bin/bitcoind /usr/local/bin/bitcoind
COPY --from=build-stage /usr/local/bin/bitcoin-cli /usr/local/bin/bitcoin-cli

# by default we expect the rpc auth cookie in this dir
RUN mkdir -p /block-data

# bitcoin.conf can be mounted over
# for a generator, see:
#   https://jlopp.github.io/bitcoin-core-config-generator/
RUN  mkdir -p /config

# add the default bitcoin.conf
# mount over /config to provide your own node config
ADD https://raw.githubusercontent.com/bitcoin/bitcoin/master/share/examples/bitcoin.conf \
    /config/bitcoin.conf

# default run command
CMD ["bitcoind", "-datadir=/block-data", "-conf=/config/bitcoin.conf"]

# expose the port to peers
EXPOSE 8333

# expose the rpc port?

#
# commands:
#
# build as:
# $ docker build -t bitcoin-core .
#
# run as:
# $ mkdir -p data/ ; docker run -d -it -p 8333:8333 --user $(id -u):$(id -g) -v $(pwd)/data:/block-data bitcoin-core
#

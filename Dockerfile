FROM debian:buster-slim AS build-env

ARG BOOST_VERSION=1.67
ARG BITCOIN_CORE_TAG=v0.18.0

RUN apt-get update && \
    apt-get install -y \
              wget unzip \
              build-essential \
              autoconf \
              libssl-dev \
              libboost$BOOST_VERISON-dev \
              libboost-chrono$BOOST_VERISON-dev \
              libboost-filesystem$BOOST_VERSION-dev \
              libboost-program-options$BOOST_VERSION-dev \
              libboost-system$BOOST_VERSION-dev \
              libboost-test$BOOST_VERSION-dev \
              libboost-thread$BOOST_VERSION-dev \
              libtool \
              pkg-config \
              libevent-dev \
              git \
              bsdmainutils \
              libzmq3-dev \
              tree

RUN mkdir /home/btc/
#RUN git clone \
#      -b $BITCOIN_CORE_TAG \
#      https://github.com/bitcoin/bitcoin.git \
#      /home/btc/bitcoin
#
WORKDIR /home/btc/
#RUN ./autogen.sh
#RUN ./configure \
#      CPPFLAGS="-I/usr/local/BerkeleyDB.4.8/include -O2" \
#      LDFLAGS="-L/usr/local/BerkeleyDB.4.8/lib" \
#      --without-gui
#
#RUN make && make install

ADD https://bitcoin.org/bin/bitcoin-core-0.18.0/bitcoin-0.18.0-x86_64-linux-gnu.tar.gz .
RUN tar -xvf bitcoin-0.18.0-x86_64-linux-gnu.tar.gz && \
    cp /home/btc/bitcoin-0.18.0/bin/bitcoin-cli /usr/local/bin && \
    cp /home/btc/bitcoin-0.18.0/bin/bitcoind /usr/local/bin && \
    rm -drf bitcoin-0.18.0

# add the default bitcoin.conf
ADD https://raw.githubusercontent.com/bitcoin/bitcoin/master/share/examples/bitcoin.conf \
    /home/btc/bitcoin.conf

# build the deployable
FROM debian:buster-slim

ARG BOOST_VERSION=1.67.0

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
              libssl1.1 \
              libboost-chrono$BOOST_VERSION \
              libboost-filesystem$BOOST_VERSION \
              libboost-thread$BOOST_VERSION \
              libevent-2.1-6 \
              libevent-pthreads-2.1-6 \
    && \
    rm -rf /var/lib/apt/lists/*

COPY --from=build-env /usr/local/bin/bitcoind /usr/local/bin/bitcoind
COPY --from=build-env /usr/local/bin/bitcoin-cli /usr/local/bin/bitcoin-cli

# by default we expect the rpc auth cookie in this dir
RUN mkdir -p /block-data

# bitcoin.conf can be mounted over
# for a generator, see:
#   https://jlopp.github.io/bitcoin-core-config-generator/
RUN  mkdir -p /config
COPY --from=build-env /home/btc/bitcoin.conf /config/bitcoin.conf

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

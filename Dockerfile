FROM debian:buster-slim AS build-env

RUN apt-get update && \
    apt-get install -y \
              build-essential \
              autoconf \
              libssl-dev \
              libboost-dev \
              libboost-chrono-dev \
              libboost-filesystem-dev \
              libboost-program-options-dev \
              libboost-system-dev \
              libboost-test-dev \
              libboost-thread-dev \
              libtool \
              pkg-config \
              libevent-dev \
              git \
              bsdmainutils

RUN mkdir /home/bitc/
RUN git clone -b v0.18.0 https://github.com/bitcoin/bitcoin.git /home/bitc/bitcoin

WORKDIR /home/bitc/bitcoin
RUN ./autogen.sh
RUN ./configure \
      CPPFLAGS="-I/usr/local/BerkeleyDB.4.8/include -O2" \
      LDFLAGS="-L/usr/local/BerkeleyDB.4.8/lib" \
      --disable-wallet

RUN make && make install

FROM debian:buster-slim

RUN useradd -ms /bin/bash bitc
WORKDIR /home/bitc

COPY --from=build-env /usr/local/bin/bitcoind /usr/local/bin/bitcoind
COPY --from=build-env /usr/local/bin/bitcoin-cli /usr/local/bin/bitcoin-cli

WORKDIR /home/bitc

CMD ["bitcoind", "-rpcuser=us", "-rpcpassword=ass"]


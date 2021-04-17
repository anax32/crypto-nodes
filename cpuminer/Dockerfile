from debian

run apt-get update; apt-get upgrade -y; \
    apt-get install -y --no-install-recommends \
      git \
      automake \
      autoconf \
      libcurl4-openssl-dev \
      libjansson-dev \
      libgmp-dev \
      build-essential \
      ca-certificates \
      libssl-dev \
      libz-dev

run cd opt ; \
    git clone https://github.com/tpruvot/cpuminer-multi

run cd /opt/cpuminer-multi ; \
    ./autogen.sh ; \
    ./configure ; \
    ./build.sh

env POOL=stratum+tcp://xmr.pool.minergate.com:45700
env USERNAME=x

cmd /opt/cpuminer-multi/cpuminer -a cryptonight -o $POOL -u $USERNAME

from debian as build

run apt-get update; apt-get upgrade -y; \
    apt-get install -y --no-install-recommends \
      autoconf \
      automake \
      build-essential \
      ca-certificates \
      git \
      libtool \
      libcurl4-openssl-dev \
      libudev-dev \
      libusb-1.0-0-dev \
      libncurses5-dev \
      libz-dev \
      pkg-config

run git clone \
      --depth 1 \
      -v \
      https://github.com/ckolivas/cgminer.git

#run git clone \
#      --single-branch \
#      --depth 1 \
#      --branch master \
#      -v \
#      https://github.com/luke-jr/bfgminer.git

run cd cgminer && \
    ./autogen.sh --enable-ants1 && \
    make

#run cd bfgminer && \
#    ./autogen.sh CFLAGS="-O2 -Wall -march=native" --enable-cpumining && \
#    make

run ls -lah /cgminer
run ls -lah /bfgminer

from debian:slim as deploy

copy --from=build /cgminer/cgminer /usr/local/bin

entrypoint cgminer

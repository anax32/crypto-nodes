# build the deployable
FROM ubuntu:16.04

# install from the bitcoin repo
RUN apt-get update && \
    apt-get install -y \
      wget \
    && \
    rm -rf /var/lib/apt/lists/*


RUN mkdir install && \
    cd install && \
    wget https://bitcoincore.org/bin/bitcoin-core-0.19.1/bitcoin-0.19.1-x86_64-linux-gnu.tar.gz && \
    tar xvf *.tar.gz && \
    cp -R */*/ /


# by default we expect the rpc auth cookie in this dir
RUN mkdir -p /block-data

# default run command
CMD ["bitcoind", "-datadir=/block-data", "-conf=/config/bitcoin.conf", "-zmqpubrawtx=tcp://127.0.0.1:23882"]

# expose the port to peers
EXPOSE 8332
EXPOSE 28832

# build the deployable
FROM ubuntu:16.04

# install from the bitcoin repo
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    apt-add-repository ppa:bitcoin/bitcoin && \
    apt-get update && \
    apt-get install -y bitcoind && \
    rm -rf /var/lib/apt/lists/*

# by default we expect the rpc auth cookie in this dir
RUN mkdir -p /block-data

# default run command
CMD ["bitcoind", "-datadir=/block-data", "-conf=/config/bitcoin.conf", "-zmqpubrawtx=tcp://127.0.0.1:23882"]

# expose the port to peers
EXPOSE 8332
EXPOSE 23882

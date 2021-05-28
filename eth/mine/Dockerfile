FROM nvidia/cuda:9.0-runtime-ubuntu16.04

ARG VERSION=0.18.0

RUN apt-get update \
    && \
    apt-get install wget

RUN wget -q -O- https://github.com/ethereum-mining/ethminer/releases/download/v$VERSION/ethminer-$VERSION-cuda-9-linux-x86_64.tar.gz | tar zxf -


ENV ETH_POOL_ADDR=eu1.ethermine.org
ENV ETH_WALLET=0xAA119411cC93b5eE0d8b54B901444aA736ABe59E
ENV WORKER_NAME=work09


CMD /bin/bash -c 'echo $ETH_WALLET ; ethminer -P stratum1+ssl://$ETH_WALLET.$WORKER_NAME@$ETH_POOL_ADDR:5555'
#CMD ethminer -P stratum1+tcp://$ETH_WALLET\%2e$WORKER_NAME@$ETH_POOL_ADDR:4444

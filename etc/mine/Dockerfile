FROM nvidia/cuda:9.0-runtime-ubuntu16.04

ARG VERSION=0.18.0

RUN apt-get update \
    && \
    apt-get install wget

RUN wget -q -O- https://github.com/ethereum-mining/ethminer/releases/download/v$VERSION/ethminer-$VERSION-cuda-9-linux-x86_64.tar.gz | tar zxf -


ENV ETC_POOL_ADDR=eu1-etc.ethermine.org
ENV ETC_WALLET=0xEa256b444298F5f9c3483fF9F46913B10117d48C
ENV WORKER_NAME=work01

CMD /bin/bash -c 'echo $ETH_WALLET ; ethminer -P stratum1+ssl://$ETC_WALLET.$WORKER_NAME@$ETC_POOL_ADDR:5555'

ARG BASE_IMAGE=nvidia/cuda:11.1-runtime
FROM $BASE_IMAGE

#ADD https://github.com/trexminer/T-Rex/releases/download/0.24.7/t-rex-0.24.7-linux-cuda11.1.tar.gz .
ADD https://github.com/trexminer/T-Rex/releases/download/0.24.7/t-rex-0.24.7-linux.tar.gz .

RUN mkdir /trex && \
    tar xf t-rex-0.24.7-linux.tar.gz -C /trex && \
    rm *.tar.gz

ENV ALGORITHM=mtp
ENV COIN=zec
ENV POOL=stratum+tcp://zec.ss.poolin.com:443
ENV USERNAME=x
ENV PASSWORD=x

CMD /trex/t-rex -a $ALGORITHM --coin $COIN -o $POOL -u $USERNAME -p $PASSWORD

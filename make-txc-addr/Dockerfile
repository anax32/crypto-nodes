ARG BASE_IMAGE=python:3.7-slim-buster
FROM $BASE_IMAGE

RUN apt-get update && \
    apt-get install -y \
      gzip \
      jq \
    && \
    pip install awscli

COPY ./copy-txcs.sh /usr/local/bin/copy-txcs.sh
COPY ./get-addrs.sh /usr/local/bin/get-addrs.sh
COPY ./cnt-addrs.sh /usr/local/bin/cnt-addrs.sh
COPY ./find-addrs.sh /usr/local/bin/find-addrs.sh
COPY ./get-transactions.sh /usr/local/bin/get-transactions.sh

# default run command

ENV PYTHONUNBUFFERED 1


ARG BASE_IMAGE=python:3.7-slim-buster
FROM $BASE_IMAGE

RUN apt-get update && \
    apt-get install -y \
      gzip \
      jq \
    && \
    pip install awscli

COPY ./copy-txcs.sh /usr/local/bin/copy-txcs.sh
COPY ./get-addresses.sh /usr/local/bin/get-addresses.sh
COPY ./count-addresses.sh /usr/local/bin/count-addresses.sh
COPY ./get-transactions.sh /usr/local/bin/get-transactions.sh

# default run command

ENV PYTHONUNBUFFERED 1


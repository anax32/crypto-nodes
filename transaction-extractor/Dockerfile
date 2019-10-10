ARG BASE_IMAGE=python:3.7-slim-buster
FROM $BASE_IMAGE

RUN apt-get update && \
    apt-get install -y \
      gzip \
      jq \
    && \
    rm -rf /var/lib/apt/lists/* \
    && \
    pip install --no-cache-dir \
      awscli

COPY ./get-addresses.sh /usr/local/bin/get-addresses.sh
COPY ./count-addresses.sh /usr/local/bin/count-addresses.sh
COPY ./get-transaction-ids.sh /usr/local/bin/get-transaction-ids.sh

# default run command

ENV PYTHONUNBUFFERED 1


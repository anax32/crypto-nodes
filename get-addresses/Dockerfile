ARG BASE_IMAGE=python:3.7-slim-buster
FROM $BASE_IMAGE

RUN pip install --no-cache-dir \
      awscli

COPY ./copy-txcs.sh /usr/local/bin/copy-txcs.sh
COPY ./get-addrs.sh /usr/local/bin/get-addrs.sh
COPY ./cnt-addrs.sh /usr/local/bin/cnt-addrs.sh
COPY ./find-addrs.sh /usr/local/bin/find-addrs.sh

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/copy-txcs.sh && /usr/local/bin/get-addrs.sh"]

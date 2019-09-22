FROM python:3.7-alpine

RUN apk update && \
    apk add --no-cache --virtual build-dependencies \
      g++ \
      python3-dev \
      zeromq-dev \
      linux-headers \
    && \
    python3 -m pip install --no-cache-dir \
      pyzmq \
      requests \
    && \
    apk del build-dependencies


RUN pip3 install --no-cache-dir \
       pyzmq \
       pymongo \
       requests



COPY ./zmq_c.py /usr/local/bin/zmq_c.py
COPY ./textwriter.py /usr/local/bin/textwriter.py
COPY ./mongowriter.py /usr/local/bin/mongowriter.py
COPY ./bitcoindrpc.py /usr/local/bin/bitcoindrpc.py

# default run command

ENV PYTHONUNBUFFERED 1

CMD ["python3", "-u", "/usr/local/bin/zmq_c.py"]
